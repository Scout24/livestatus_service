import unittest
import tempfile
from mock import patch, call


from livestatus_service.configuration import Configuration, get_current_configuration

class ConfigurationTests(unittest.TestCase):

    def test_constructor_should_raise_exception_when_config_file_does_not_exist(self):
        def callback():
            Configuration(("/foo/bar/does_not_exist.cfg"))

        self.assertRaises(ValueError, callback)


    def test_constructor_should_raise_exception_when_config_file_has_invalid_content(self):
        with tempfile.NamedTemporaryFile() as configuration_file:
            configuration_file.write('foobar')
            def callback():
                Configuration(configuration_file.name)
            self.assertRaises(ValueError, callback)



    def test_constructor_should_raise_exception_when_config_does_not_contain_expected_section(self):
        with tempfile.NamedTemporaryFile() as configuration_file:
            configuration_file.write(b"[spam]\nspam=eggs")
            def callback():
                Configuration(configuration_file.name)
            self.assertRaises(ValueError, callback)



    def test_should_return_default_log_file_when_no_log_file_option_is_given(self):
        with tempfile.NamedTemporaryFile() as configuration_file:
            configuration_file.write(b"[{0}]\n".format(Configuration.SECTION))
            configuration_file.flush()
            config = Configuration(configuration_file.name)
            self.assertEquals(config.log_file, Configuration.DEFAULT_LOG_FILE)



    def test_should_return_given_log_file_when_log_file_option_is_given(self):
        with tempfile.NamedTemporaryFile() as configuration_file:
            configuration_file.write(b"[{0}]\n{1}=spam.log".format(Configuration.SECTION, Configuration.OPTION_LOG_FILE))
            configuration_file.flush()
            config = Configuration(configuration_file.name)
            self.assertEquals(config.log_file, "spam.log")


    def test_should_return_default_livestatus_socket(self):
        with tempfile.NamedTemporaryFile() as configuration_file:
            configuration_file.write(b"[{0}]\n".format(Configuration.SECTION))
            configuration_file.flush()
            config = Configuration(configuration_file.name)
            self.assertEquals(config.livestatus_socket, Configuration.DEFAULT_LIVESTATUS_SOCKET)


    def test_should_return_configured_livestatus_socket(self):
        with tempfile.NamedTemporaryFile() as configuration_file:
            configuration_file.write(b"[{0}]\n{1}=foo/bar".format(Configuration.SECTION, Configuration.OPTION_LIVESTATUS_SOCKET))
            configuration_file.flush()
            config = Configuration(configuration_file.name)
            self.assertEquals(config.livestatus_socket, "foo/bar")


    def test_should_return_default_icinga_command_file(self):
        with tempfile.NamedTemporaryFile() as configuration_file:
            configuration_file.write(b"[{0}]\n".format(Configuration.SECTION))
            configuration_file.flush()
            config = Configuration(configuration_file.name)
            self.assertEquals(config.icinga_command_file, Configuration.DEFAULT_ICINGA_COMMAND_FILE)


    def test_should_return_configured_icinga_command_file(self):
        with tempfile.NamedTemporaryFile() as configuration_file:
            configuration_file.write(b"[{0}]\n{1}=foo/bar.cmd".format(Configuration.SECTION, Configuration.OPTION_ICINGA_COMMAND_FILE))
            configuration_file.flush()
            config = Configuration(configuration_file.name)
            self.assertEquals(config.icinga_command_file, "foo/bar.cmd")


class ConfigurationLoadingTests(unittest.TestCase):

    @patch('livestatus_service.configuration.Configuration')
    def test_get_current_configuration_should_open_default_configuration_file(self, mock_configuration):
        get_current_configuration()

        self.assertEqual(mock_configuration.call_args, call(mock_configuration.DEFAULT_CONFIGURATION_FILE))
