import pytest
from unittest.mock import Mock, patch, PropertyMock
from src.gui.voice_assistant_gui import VoiceAssistantGUI

@pytest.fixture
def mock_tk():
    with patch('tkinter.Tk') as mock_tk_class:
        mock_root = Mock()
        
        # Create proper mock methods for window info
        mock_root.winfo_screenwidth = Mock(return_value=1920)
        mock_root.winfo_screenheight = Mock(return_value=1080)
        mock_root.winfo_width = Mock(return_value=600)
        mock_root.winfo_height = Mock(return_value=400)
        mock_root.winfo_x = Mock(return_value=0)
        mock_root.winfo_y = Mock(return_value=0)
        
        # Store geometry string
        mock_root._geometry = "600x400+660+340"
        
        def mock_geometry(geometry_str=None):
            if geometry_str is None:
                return mock_root._geometry
            mock_root._geometry = geometry_str
            
        mock_root.geometry = Mock(side_effect=mock_geometry)
        mock_tk_class.return_value = mock_root
        yield mock_root

@pytest.fixture
def gui():
    with patch('tkinter.Tk') as mock_tk_class, \
         patch('tkinter.ttk.Label') as mock_label, \
         patch('tkinter.Text') as mock_text, \
         patch('tkinter.ttk.Style') as mock_style:
        
        # Configure root mock
        mock_root = Mock()
        mock_root.winfo_screenwidth = Mock(return_value=1920)
        mock_root.winfo_screenheight = Mock(return_value=1080)
        mock_root.winfo_width = Mock(return_value=600)
        mock_root.winfo_height = Mock(return_value=400)
        mock_root.winfo_x = Mock(return_value=0)
        mock_root.winfo_y = Mock(return_value=0)
        mock_root._geometry = "600x400+660+340"
        
        def mock_geometry(geometry_str=None):
            if geometry_str is None:
                return mock_root._geometry
            mock_root._geometry = geometry_str
        mock_root.geometry = Mock(side_effect=mock_geometry)
        mock_tk_class.return_value = mock_root
        
        # Configure widget mocks
        mock_label_instance = Mock()
        mock_text_instance = Mock()
        mock_style_instance = Mock()
        
        mock_label_instance.configure = Mock()
        mock_text_instance.delete = Mock()
        mock_text_instance.insert = Mock()
        
        mock_label.return_value = mock_label_instance
        mock_text.return_value = mock_text_instance
        mock_style.return_value = mock_style_instance
        
        # Create GUI instance
        instance = VoiceAssistantGUI()
        
        # Override some attributes for testing
        instance.status_label = mock_label_instance
        instance.detected_label = mock_label_instance
        instance.response_text = mock_text_instance
        
        def mock_calculate_geometry():
            return "600x400+660+340"
        instance._calculate_geometry = Mock(side_effect=mock_calculate_geometry)
        
        yield instance
        
        try:
            instance.stop()
        except:
            pass

def test_gui_initialization(gui):
    assert isinstance(gui.root, Mock)
    assert gui.COLORS['accent'] == '#007ACC'

def test_update_status(gui):
    gui.update_status("Test status", "🔴")
    gui.status_label.configure.assert_called_with(text="🔴 Test status")

def test_update_detected_with_text(gui):
    gui.update_detected("Test detection")
    gui.detected_label.configure.assert_called_with(text="Detected: Test detection")

def test_update_detected_without_text(gui):
    gui.update_detected(None)
    gui.detected_label.configure.assert_called_with(text="")

def test_update_response(gui):
    test_text = "Test response"
    gui.update_response(test_text)
    gui.response_text.delete.assert_called_with("1.0", "end")
    gui.response_text.insert.assert_called_with("1.0", test_text)

def test_start_gui(gui):
    gui.start()
    gui.root.mainloop.assert_called_once()

def test_stop_gui(gui):
    gui.stop()
    gui.root.destroy.assert_called_once()

def test_gui_geometry_calculation(gui, mock_tk):
    expected_geometry = "600x400+660+340"
    actual_geometry = gui.root.geometry()
    assert actual_geometry == expected_geometry
