import requests
import json
from datetime import datetime


class SimpleLife360:
    """Simplified Life360 API client for getting member information and locations"""

    def __init__(self, username, password):
        self.base_url = "https://api-cloudfront.life360.com/"
        self.username = username
        self.password = password
        self.access_token = None
        self.authorization_token = "Y2F0aGFwYWNyQVBoZUtVc3RlOGV2ZXZldnVjSGFmZVRydVl1ZnJhYzpkOEM5ZVlVdkE2dUZ1YnJ1SmVnZXRyZVZ1dFJlQ1JVWQ=="
        self.user_agent = "com.life360.android.safetymapd/KOKO/23.49.0 android/13"

    def _make_request(self, url, method='GET', data=None, auth_header=None):
        """Make HTTP request to Life360 API"""
        headers = {
            'Accept': 'application/json',
            'user-agent': self.user_agent
        }

        if auth_header:
            headers['Authorization'] = auth_header
            headers['cache-control'] = "no-cache"

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(
                    url, data=data, headers=headers, timeout=30)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def authenticate(self):
        """Authenticate with Life360 and get access token"""
        url = f"{self.base_url}v3/oauth2/token"
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
        }

        auth_header = f"Basic {self.authorization_token}"
        result = self._make_request(
            url, method='POST', data=data, auth_header=auth_header)

        if result and 'access_token' in result:
            self.access_token = result['access_token']
            print("✅ Authentication successful!")
            return True
        else:
            print("❌ Authentication failed!")
            return False

    def get_circles(self):
        """Get all circles for the authenticated user"""
        if not self.access_token:
            print("Not authenticated. Please authenticate first.")
            return None

        url = f"{self.base_url}v4/circles"
        auth_header = f"bearer {self.access_token}"
        result = self._make_request(url, auth_header=auth_header)

        if result and 'circles' in result:
            return result['circles']
        return None

    def get_circle_members(self, circle_id):
        """Get all members in a specific circle"""
        if not self.access_token:
            print("Not authenticated. Please authenticate first.")
            return None

        url = f"{self.base_url}v4/circles/{circle_id}/members"
        auth_header = f"bearer {self.access_token}"
        result = self._make_request(url, auth_header=auth_header)

        if result and 'members' in result:
            return result['members']
        return None

    def get_member_location(self, circle_id, member_id):
        """Get location data for a specific member"""
        if not self.access_token:
            print("Not authenticated. Please authenticate first.")
            return None

        # First, make a location request
        url = f"{self.base_url}v3/circles/{circle_id}/members/{member_id}/request"
        auth_header = f"bearer {self.access_token}"
        request_result = self._make_request(
            url, method='POST', data={"type": "location"}, auth_header=auth_header)

        if request_result and 'requestId' in request_result:
            # Then fetch the actual location data
            request_id = request_result['requestId']
            url = f"{self.base_url}v3/circles/members/request/{request_id}"
            location_result = self._make_request(url, auth_header=auth_header)
            return location_result
        return None

    def get_all_members_info(self):
        """Get all members' information and locations from all circles"""
        all_members_data = []

        # Get all circles
        circles = self.get_circles()
        if not circles:
            print("No circles found.")
            return all_members_data

        print(f"\n📍 Found {len(circles)} circle(s)")

        for circle in circles:
            circle_id = circle['id']
            circle_name = circle.get('name', 'Unnamed Circle')
            print(f"\n🔵 Circle: {circle_name}")

            # Get members in this circle
            members = self.get_circle_members(circle_id)
            if not members:
                print("  No members found in this circle.")
                continue

            print(f"  Found {len(members)} member(s)")

            for member in members:
                member_data = {
                    'circle_name': circle_name,
                    'circle_id': circle_id,
                    'member_id': member['id'],
                    'first_name': member.get('firstName', ''),
                    'last_name': member.get('lastName', ''),
                    'email': member.get('loginEmail', ''),
                    'phone': member.get('loginPhone', ''),
                    'avatar': member.get('avatar', ''),
                    'location': None
                }

                # Get location data for this member
                print(
                    f"  👤 {member_data['first_name']} {member_data['last_name']}")
                location_data = self.get_member_location(
                    circle_id, member['id'])

                if location_data and 'location' in location_data and location_data['location']:
                    location = location_data['location']
                    member_data['location'] = {
                        'latitude': location.get('latitude'),
                        'longitude': location.get('longitude'),
                        'battery': location.get('battery'),
                        'charging': location.get('charge'),
                        'in_transit': location.get('inTransit'),
                        'speed': location.get('speed'),
                        'since': datetime.fromtimestamp(int(location.get('since', 0))).isoformat() if location.get('since') else None,
                        'address': location.get('address1', '')
                    }
                    print(
                        f"    📍 Location: {location.get('latitude')}, {location.get('longitude')}")
                    print(f"    🔋 Battery: {location.get('battery')}%")
                else:
                    print(f"    ❌ Location not available")

                all_members_data.append(member_data)

        return all_members_data


# Example usage
if __name__ == "__main__":
    # Replace with your Life360 credentials
    USERNAME = "username@gmail.com"
    PASSWORD = "password"

    # Create client instance
    client = SimpleLife360(USERNAME, PASSWORD)

    # Authenticate
    if client.authenticate():
        # Get all members' information
        members_data = client.get_all_members_info()

        # Save to JSON file
        with open('life360_members_data.json', 'w') as f:
            json.dump(members_data, f, indent=2)

        print(f"\n✅ Data saved to life360_members_data.json")
        print(f"Total members found: {len(members_data)}")

        # Print summary
        print("\n📊 Summary:")
        for member in members_data:
            name = f"{member['first_name']} {member['last_name']}"
            circle = member['circle_name']
            has_location = "✅" if member['location'] else "❌"
            print(f"  {name} (Circle: {circle}) - Location: {has_location}")
