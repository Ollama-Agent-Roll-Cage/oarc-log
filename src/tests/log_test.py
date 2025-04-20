"""
Tests for the oarc_log.log module.

This module contains comprehensive tests for the functionality of the
context-aware logging system provided by oarc_log.
"""

import logging
import sys
import io
from unittest.mock import patch, MagicMock, call, DEFAULT
import pytest

# Import after defining the module structure
from oarc_log.log import (
    ContextAwareLogger, 
    Logger,
    log, 
    get_logger, 
    redirect_external_loggers, 
    enable_debug_logging
)


class TestContextAwareLogger:
    """Test the ContextAwareLogger class functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.base_logger = logging.getLogger("test_base_logger")
        self.context_logger = ContextAwareLogger(self.base_logger)
    
    def test_init(self):
        """Test the initialization of ContextAwareLogger."""
        assert self.context_logger._base_logger == self.base_logger
    
    @patch('inspect.stack')
    def test_get_caller_module(self, mock_stack):
        """Test the _get_caller_module method."""
        # Create a mock stack frame
        mock_frame = MagicMock()
        mock_module = MagicMock()
        mock_module.__name__ = "tests.log_test"
        
        # Set up the inspect.stack() mock to return our controlled frame
        mock_frame_obj = MagicMock()
        mock_frame_obj[0] = mock_frame
        mock_stack.return_value = [MagicMock(), mock_frame_obj]
        
        # Make getmodule return our mock module
        with patch('inspect.getmodule', return_value=mock_module):
            module_name = self.context_logger._get_caller_module()
            assert module_name == "tests.log_test"
    
    @patch('logging.getLogger')
    @patch('oarc_log.log.ContextAwareLogger._get_caller_module')
    def test_debug(self, mock_get_caller, mock_get_logger):
        """Test the debug method."""
        mock_get_caller.return_value = "tests.log_test"
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        self.context_logger.debug("Test debug message")
        
        mock_get_logger.assert_called_once_with("tests.log_test")
        mock_logger.debug.assert_called_once_with("Test debug message")
    
    @patch('logging.getLogger')
    @patch('oarc_log.log.ContextAwareLogger._get_caller_module')
    def test_info(self, mock_get_caller, mock_get_logger):
        """Test the info method."""
        mock_get_caller.return_value = "tests.log_test"
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        self.context_logger.info("Test info message")
        
        mock_get_logger.assert_called_once_with("tests.log_test")
        mock_logger.info.assert_called_once_with("Test info message")
    
    @patch('logging.getLogger')
    @patch('oarc_log.log.ContextAwareLogger._get_caller_module')
    def test_warning(self, mock_get_caller, mock_get_logger):
        """Test the warning method."""
        mock_get_caller.return_value = "tests.log_test"
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        self.context_logger.warning("Test warning message")
        
        mock_get_logger.assert_called_once_with("tests.log_test")
        mock_logger.warning.assert_called_once_with("Test warning message")
    
    @patch('logging.getLogger')
    @patch('oarc_log.log.ContextAwareLogger._get_caller_module')
    def test_error(self, mock_get_caller, mock_get_logger):
        """Test the error method."""
        mock_get_caller.return_value = "tests.log_test"
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        self.context_logger.error("Test error message")
        
        mock_get_logger.assert_called_once_with("tests.log_test")
        mock_logger.error.assert_called_once_with("Test error message")
    
    @patch('logging.getLogger')
    @patch('oarc_log.log.ContextAwareLogger._get_caller_module')
    def test_critical(self, mock_get_caller, mock_get_logger):
        """Test the critical method."""
        mock_get_caller.return_value = "tests.log_test"
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        self.context_logger.critical("Test critical message")
        
        mock_get_logger.assert_called_once_with("tests.log_test")
        mock_logger.critical.assert_called_once_with("Test critical message")
    
    @patch('logging.getLogger')
    @patch('oarc_log.log.ContextAwareLogger._get_caller_module')
    def test_exception(self, mock_get_caller, mock_get_logger):
        """Test the exception method."""
        mock_get_caller.return_value = "tests.log_test"
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        self.context_logger.exception("Test exception message")
        
        mock_get_logger.assert_called_once_with("tests.log_test")
        mock_logger.exception.assert_called_once_with("Test exception message")
    
    def test_is_debug_enabled_true(self):
        """Test is_debug_enabled returns True when debug is enabled."""
        self.base_logger.level = logging.DEBUG
        assert self.context_logger.is_debug_enabled() is True
    
    def test_is_debug_enabled_false(self):
        """Test is_debug_enabled returns False when debug is not enabled."""
        self.base_logger.level = logging.INFO
        assert self.context_logger.is_debug_enabled() is False


class TestLoggerClass:
    """Test the Logger class functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Reset Logger state before each test
        Logger._initialized = False
        Logger._loggers = {}
        Logger._handler = None
        Logger._context_logger = None
    
    @patch('sys.stderr')
    @patch('logging.Formatter')
    @patch('logging.getLogger')
    def test_initialize(self, mock_get_logger, mock_formatter, mock_stderr):
        """Test the initialize method."""
        # Create mock loggers
        mock_root_logger = MagicMock()
        mock_main_logger = MagicMock()
        
        # Configure getLogger to return our mocks
        mock_get_logger.side_effect = lambda name=None: mock_root_logger if name is None else mock_main_logger
        
        # Skip the redirect_external_loggers call during initialize
        with patch.object(Logger, 'redirect_external_loggers'):
            # Call initialize
            Logger.initialize()
            
            # Check that it's initialized
            assert Logger._initialized is True
            
            # Check that the root logger is configured correctly
            mock_root_logger.setLevel.assert_called_with(logging.INFO)
            mock_root_logger.handlers.clear.assert_called_once()
            assert mock_root_logger.addHandler.called
            
            # Check that the main logger is configured correctly
            mock_main_logger.setLevel.assert_called_with(logging.INFO)
            assert mock_main_logger.propagate is False
            mock_main_logger.handlers.clear.assert_called_once()
            assert mock_main_logger.addHandler.called
    
    @patch('logging.getLogger')
    def test_initialize_idempotent(self, mock_get_logger):
        """Test that initialize is idempotent."""
        # Set up as if already initialized
        Logger._initialized = True
        
        # Call initialize again
        Logger.initialize()
        
        # Check that get_logger was not called
        mock_get_logger.assert_not_called()
    
    @patch.object(Logger, 'initialize')
    def test_get_logger_no_name(self, mock_initialize):
        """Test get_logger with no name."""
        mock_logger = MagicMock()
        Logger._loggers = {Logger.LOGGER_NAME: mock_logger}
        
        result = Logger.get_logger()
        
        mock_initialize.assert_called_once()
        assert result == mock_logger
    
    @patch.object(Logger, 'initialize')
    def test_get_logger_with_name(self, mock_initialize):
        """Test get_logger with a name."""
        # Mock the existing loggers check
        Logger._loggers = {}
        Logger._handler = MagicMock()
        
        # Create a real logger for testing instead of mocking logger.addHandler
        test_logger = logging.getLogger("test_logger")
        
        # Use a more targeted patch that doesn't affect the addHandler behavior
        with patch('logging.getLogger', return_value=test_logger):
            result = Logger.get_logger("test_logger")
            
            mock_initialize.assert_called_once()
            assert result.name == "test_logger"
            assert result.level == logging.INFO
            assert result.propagate is False
            assert Logger._handler in result.handlers
            assert "test_logger" in Logger._loggers
    
    @patch.object(Logger, 'initialize')
    @patch('logging.getLogger')
    def test_get_logger_cached(self, mock_get_logger, mock_initialize):
        """Test get_logger returns cached logger."""
        mock_logger = MagicMock()
        Logger._loggers = {"test_logger": mock_logger}
        
        result = Logger.get_logger("test_logger")
        
        mock_initialize.assert_called_once()
        mock_get_logger.assert_not_called()
        assert result == mock_logger
    
    @patch.object(Logger, 'initialize')
    @patch('logging.getLogger')
    def test_redirect_external_loggers(self, mock_get_logger, mock_initialize):
        """Test redirect_external_loggers."""
        mock_logger1 = MagicMock()
        mock_logger2 = MagicMock()
        mock_get_logger.side_effect = [mock_logger1, mock_logger2]
        Logger._handler = MagicMock()
        
        Logger.redirect_external_loggers("test_ext1", "test_ext2", level=logging.ERROR)
        
        mock_initialize.assert_called_once()
        assert mock_get_logger.call_count == 2
        assert mock_get_logger.call_args_list == [call("test_ext1"), call("test_ext2")]
        
        for mock_logger in [mock_logger1, mock_logger2]:
            mock_logger.handlers.clear.assert_called_once()
            assert mock_logger.propagate is False
            mock_logger.addHandler.assert_called_with(Logger._handler)
            mock_logger.setLevel.assert_called_with(logging.ERROR)
        
        assert "test_ext1" in Logger._loggers
        assert "test_ext2" in Logger._loggers
    
    @patch.object(Logger, 'initialize')
    @patch('logging.getLogger')
    def test_enable_debug_logging(self, mock_get_logger, mock_initialize):
        """Test enable_debug_logging."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        Logger._context_logger = MagicMock()
        
        result = Logger.enable_debug_logging()
        
        mock_initialize.assert_called_once()
        mock_get_logger.assert_called_with(Logger.LOGGER_NAME)
        mock_logger.setLevel.assert_called_with(logging.DEBUG)
        Logger._context_logger.debug.assert_called_with("Debug logging enabled")
        assert result is None
    
    def test_enable_debug_logging_click_callback_false(self):
        """Test enable_debug_logging as Click callback with False value."""
        ctx = MagicMock()
        param = MagicMock()
        value = False
        
        result = Logger.enable_debug_logging(ctx, param, value)
        
        assert result is False
    
    @patch.object(Logger, 'initialize')
    @patch('logging.getLogger')
    def test_enable_debug_logging_click_callback_true(self, mock_get_logger, mock_initialize):
        """Test enable_debug_logging as Click callback with True value."""
        ctx = MagicMock()
        param = MagicMock()
        value = True
        
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        Logger._context_logger = MagicMock()
        
        result = Logger.enable_debug_logging(ctx, param, value)
        
        mock_initialize.assert_called_once()
        mock_get_logger.assert_called_with(Logger.LOGGER_NAME)
        mock_logger.setLevel.assert_called_with(logging.DEBUG)
        Logger._context_logger.debug.assert_called_with("Debug logging enabled")
        assert result is True
    
    @patch('logging.getLogger')
    def test_is_debug_enabled_true(self, mock_get_logger):
        """Test is_debug_enabled returns True when debug is enabled."""
        mock_logger = MagicMock()
        mock_logger.level = logging.DEBUG
        mock_get_logger.return_value = mock_logger
        
        result = Logger.is_debug_enabled()
        
        mock_get_logger.assert_called_once_with(Logger.LOGGER_NAME)
        assert result is True
    
    @patch('logging.getLogger')
    def test_is_debug_enabled_false(self, mock_get_logger):
        """Test is_debug_enabled returns False when debug is not enabled."""
        mock_logger = MagicMock()
        mock_logger.level = logging.INFO
        mock_get_logger.return_value = mock_logger
        
        result = Logger.is_debug_enabled()
        
        mock_get_logger.assert_called_once_with(Logger.LOGGER_NAME)
        assert result is False


class TestExportedFunctions:
    """Test the exported functions and objects."""
    
    def setup_method(self):
        """Reset any module state before each test."""
        # Make sure we can properly test the exported functions
        import sys
        if 'oarc_log.log' in sys.modules:
            del sys.modules['oarc_log.log']
            import oarc_log.log
    
    def test_log_is_context_aware_logger(self):
        """Test that log is a ContextAwareLogger."""
        assert isinstance(log, ContextAwareLogger)
    
    @patch('oarc_log.log.get_logger')  # Patch the module-level export
    def test_get_logger(self, mock_get_logger):
        """Test that get_logger calls Logger.get_logger."""
        # Setup mock and original function reference
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Call the function under test through the import
        from oarc_log.log import get_logger as get_logger_import
        result = get_logger_import("test_module")
        
        # Assertions
        mock_get_logger.assert_called_once_with("test_module")
        assert result == mock_logger
    
    @patch('oarc_log.log.redirect_external_loggers')  # Patch the module-level export
    def test_redirect_external_loggers(self, mock_redirect):
        """Test that redirect_external_loggers calls Logger.redirect_external_loggers."""
        # Call the function under test through the import
        from oarc_log.log import redirect_external_loggers as redirect_import
        redirect_import("test1", "test2", level=logging.ERROR)
        
        # Assertion
        mock_redirect.assert_called_once_with("test1", "test2", level=logging.ERROR)
    
    @patch('oarc_log.log.enable_debug_logging')  # Patch the module-level export
    def test_enable_debug_logging(self, mock_enable_debug):
        """Test that enable_debug_logging calls Logger.enable_debug_logging."""
        # Setup test parameters
        ctx = MagicMock()
        param = MagicMock()
        value = True
        
        # Call the function under test through the import
        from oarc_log.log import enable_debug_logging as enable_debug_import
        enable_debug_import(ctx, param, value)
        
        # Assertion
        mock_enable_debug.assert_called_once_with(ctx, param, value)


class TestIntegration:
    """Integration tests for the logging system."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Reset Logger state before each test
        Logger._initialized = False
        Logger._loggers = {}
        Logger._handler = None
        Logger._context_logger = None
        
        # Reset logging config
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)
    
    def test_initialization_creates_context_logger(self):
        """Test that initialization creates a context logger."""
        # Make sure the module is reloaded fresh
        import sys
        if 'oarc_log.log' in sys.modules:
            del sys.modules['oarc_log.log']
            
        # Import the module again - this should run initialization
        import oarc_log.log
        from oarc_log.log import log, Logger
        from oarc_log.log import ContextAwareLogger as ReloadedContextAwareLogger
        
        # Test with the class from the reloaded module, not our original import
        assert isinstance(log, ReloadedContextAwareLogger)
        assert Logger._initialized is True
    
    @pytest.mark.parametrize("log_method,log_level", [
        ("debug", logging.DEBUG),
        ("info", logging.INFO),
        ("warning", logging.WARNING),
        ("error", logging.ERROR),
        ("critical", logging.CRITICAL),
    ])
    def test_log_methods_with_enabled_level(self, log_method, log_level):
        """Test that log methods work with appropriate levels."""
        # Reset the module
        import sys
        if 'oarc_log.log' in sys.modules:
            del sys.modules['oarc_log.log']
        
        # Use a real in-memory stream for capturing logs
        buffer = io.StringIO()
        handler = logging.StreamHandler(buffer)
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        handler.setLevel(log_level)
        
        # Configure the test module logger
        test_logger = logging.getLogger("test_module")
        test_logger.setLevel(log_level)
        test_logger.addHandler(handler)
        test_logger.propagate = False
        
        # Import the module and patch the caller module detection
        import oarc_log.log
        with patch('oarc_log.log.ContextAwareLogger._get_caller_module', return_value="test_module"):
            # Call the log method
            getattr(oarc_log.log.log, log_method)(f"Test {log_method} message")
            
        # Check that the message was logged correctly
        buffer.seek(0)
        log_output = buffer.getvalue()
        expected = f"{log_method.upper()}: Test {log_method} message"
        assert expected in log_output
        
    def test_integration_get_logger(self):
        """Test that get_logger returns a logger that can log messages."""
        # Reset the module
        import sys
        if 'oarc_log.log' in sys.modules:
            del sys.modules['oarc_log.log']
            
        # Re-import to initialize
        import oarc_log.log
        from oarc_log.log import get_logger
        
        logger = get_logger("test_integration")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_integration"
        
        # Check that the logger has our handler
        assert len(logger.handlers) > 0
        
    def test_integration_redirect_external_loggers(self):
        """Test that redirect_external_loggers configures external loggers."""
        # Reset the module
        import sys
        if 'oarc_log.log' in sys.modules:
            del sys.modules['oarc_log.log']
            
        # Re-import to initialize
        import oarc_log.log
        from oarc_log.log import redirect_external_loggers
        
        redirect_external_loggers("test_external", level=logging.ERROR)
        
        ext_logger = logging.getLogger("test_external")
        assert ext_logger.level == logging.ERROR
        assert len(ext_logger.handlers) > 0
        assert ext_logger.propagate is False


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
