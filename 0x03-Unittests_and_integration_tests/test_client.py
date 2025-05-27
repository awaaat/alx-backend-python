import unittest
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
import client

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class from client module"""
    @parameterized.expand([
        ('google_org', 'google', {'login': 'google', 'repo_url': 'https://api.github.com/orgs/google/repos'}),
        ('abc_org', 'abc', {'login': 'abc', 'repo_url': 'https://api.github.com/orgs/abc/repos'})
    ])
    @patch('client.get_json')
    def test_org(self, name, organization_name, expected_data, mock_get_json):
        mock_get_json.return_value = expected_data
        org_client = GithubOrgClient(organization_name)
        self.assertEqual(org_client.org, expected_data, f"The organization {organization_name} should provided expected results {expected_data}")
        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{organization_name}')
    
    def test_public_repos_url(self):
        payload = {"repos_url": "https://example.com/example_org/repos"}
        with patch('client.GithubOrgClient.org', new_callable = PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient('example_org')
            self.assertEqual(client._public_repos_url, "https://example.com/example_org/repos", f"Should return repository URL")
    
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos.

        Args:
            mock_get_json (_type_): _description_
        """
        test_repos = [
            {'name': 'repo_1', 'license': "license_for_repo_1"},
            {'name': 'repo_2', 'license': 'license for repo_2'}
        ]
        mock_get_json.return_value = test_repos
        with patch('client.GithubOrgClient._public_repos_url', new_callable = PropertyMock) as mock_url:
            mock_url.return_value = 'https://api.github.com/example_org/repos'
            client = GithubOrgClient('example_org')
            self.assertEqual(client.public_repos(), ['repo_1', 'repo_2'], 'Should return a list of repository names')
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/example_org/repos")
    
    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False)
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected, 'Should return a license key' )
    
@parameterized_class([{
    'org_payload': {'repos_url': "https://api.github.com/example_org/repos"}, 
    'repos_payload': [{'name': 'repo_1'}, {'name': 'repo_2'}],
    'expected_repos': ['repo_1', 'repo_2']
}])    
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            Mock(json=Mock(return_value=cls.org_payload)),
            Mock(json=Mock(return_value=cls.repos_payload))
        ]

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient('test')
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)