import unittest
from unittest.mock import Mock, patch

import iniciar


class LauncherTests(unittest.TestCase):
    @patch('iniciar.webbrowser.open', return_value=True)
    @patch('iniciar.subprocess.Popen')
    @patch('iniciar.is_ready', return_value=True)
    def test_reuses_own_server_and_opens_one_tab(self, ready, process, browser):
        self.assertEqual(iniciar.main(), 0)
        browser.assert_called_once_with(iniciar.URL, new=2)
        process.assert_not_called()

    @patch('iniciar.webbrowser.open')
    @patch('iniciar.subprocess.Popen')
    @patch('iniciar.port_in_use', return_value=True)
    @patch('iniciar.is_ready', return_value=False)
    def test_does_not_open_or_stop_an_unrelated_server(self, ready, busy, process, browser):
        self.assertEqual(iniciar.main(), 1)
        browser.assert_not_called()
        process.assert_not_called()

    @patch('iniciar.webbrowser.open', return_value=True)
    @patch('iniciar.wait_until_ready', return_value=True)
    @patch('iniciar.subprocess.Popen')
    @patch('iniciar.port_in_use', return_value=False)
    @patch('iniciar.is_ready', return_value=False)
    def test_opens_browser_after_owned_server_is_ready(self, ready, busy, process, wait, browser):
        server = Mock()
        process.return_value = server
        server.poll.return_value = None
        server.wait.return_value = 0
        self.assertEqual(iniciar.main(), 0)
        wait.assert_called_once_with(server)
        browser.assert_called_once_with(iniciar.URL, new=2)
        server.terminate.assert_called_once()

    @patch('iniciar.webbrowser.open')
    @patch('iniciar.wait_until_ready', return_value=False)
    @patch('iniciar.subprocess.Popen')
    @patch('iniciar.port_in_use', return_value=False)
    @patch('iniciar.is_ready', return_value=False)
    def test_startup_failure_does_not_open_browser(self, ready, busy, process, wait, browser):
        server = Mock()
        process.return_value = server
        server.poll.return_value = None
        self.assertEqual(iniciar.main(), 1)
        browser.assert_not_called()
        server.terminate.assert_called_once()


if __name__ == '__main__':
    unittest.main()
