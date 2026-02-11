# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for OpenLiveCaption
Configures single-file executable with all dependencies
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect data files for Whisper models and transformers
whisper_datas = collect_data_files('whisper')
transformers_datas = collect_data_files('transformers')
torch_datas = collect_data_files('torch')

# Collect all submodules for dynamic imports
whisper_hiddenimports = collect_submodules('whisper')
transformers_hiddenimports = collect_submodules('transformers')
torch_hiddenimports = collect_submodules('torch')

# Additional hidden imports for dynamic dependencies
hidden_imports = [
    # PyQt6 modules
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.sip',
    
    # Audio libraries
    'sounddevice',
    'soundfile',
    '_soundfile_data',
    
    # Whisper and dependencies
    'whisper',
    'tiktoken',
    'tiktoken_ext',
    'tiktoken_ext.openai_public',
    
    # PyTorch
    'torch',
    'torch.nn',
    'torch.nn.functional',
    
    # Transformers
    'transformers',
    'transformers.models',
    'transformers.models.marian',
    
    # NumPy
    'numpy',
    'numpy.core',
    'numpy.core._multiarray_umath',
    
    # Other dependencies
    'cv2',
    'tqdm',
    'regex',
    'requests',
    'urllib3',
    'certifi',
    'charset_normalizer',
    'idna',
]

# Platform-specific imports
if sys.platform == 'win32':
    hidden_imports.extend([
        'pyaudiowpatch',
        'pyaudio',
    ])

# Combine all hidden imports
all_hidden_imports = hidden_imports + whisper_hiddenimports + transformers_hiddenimports + torch_hiddenimports

# Binaries to exclude (CUDA libraries for size reduction)
excluded_binaries = []
if sys.platform == 'win32':
    excluded_binaries = [
        ('cudart64*.dll', '.', 'BINARY'),
        ('cublas64*.dll', '.', 'BINARY'),
        ('cublasLt64*.dll', '.', 'BINARY'),
        ('cudnn64*.dll', '.', 'BINARY'),
        ('cufft64*.dll', '.', 'BINARY'),
        ('curand64*.dll', '.', 'BINARY'),
        ('cusparse64*.dll', '.', 'BINARY'),
        ('cusolver64*.dll', '.', 'BINARY'),
        ('nvrtc64*.dll', '.', 'BINARY'),
    ]

a = Analysis(
    ['Main.py'],
    pathex=[],
    binaries=[],
    datas=whisper_datas + transformers_datas + torch_datas,
    hiddenimports=all_hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib',
        'scipy',
        'pandas',
        'IPython',
        'jupyter',
        'notebook',
        'tkinter',
        'test',
        'tests',
        'unittest',
        'distutils',
        'setuptools',
        'pip',
        'wheel',
        # Exclude CUDA for CPU-only build
        'torch.cuda',
        'torch.backends.cuda',
        'torch.backends.cudnn',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove excluded binaries
a.binaries = [x for x in a.binaries if not any(pattern in x[0] for pattern, _, _ in excluded_binaries)]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OpenLiveCaption',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if sys.platform == 'win32' else 'assets/icon.icns' if sys.platform == 'darwin' else None,
)

# macOS app bundle configuration
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='OpenLiveCaption.app',
        icon='assets/icon.icns',
        bundle_identifier='com.openlivecaption.app',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
            'NSMicrophoneUsageDescription': 'OpenLiveCaption needs access to your microphone to transcribe audio.',
            'NSAppleEventsUsageDescription': 'OpenLiveCaption needs to control system audio for transcription.',
        },
    )
