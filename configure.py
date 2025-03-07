#!/usr/bin/env python
import sys
import os

try:
    from ambuild2 import run, util
except:
    try:
        import ambuild
        sys.stderr.write('AMBuild 1 is no longer supported. Please upgrade to AMBuild 2.\n')
    except:
        sys.stderr.write('AMBuild must be installed to build this project.\n')
    sys.exit(1)

def make_objdir_name(p):
    return 'obj-' + p.target_platform + '-' + p.target_arch

def run_configure(args):
    cfg = run.BuildParser(args)
    cfg.options.add_option('--sdks', type=str, default='all', help='Liste des SDKs à utiliser (all, css, tf2, l4d2, etc.)')
    cfg.options.add_option('--hl2sdk-root', type=str, default=None, help='Chemin racine pour les HL2SDKs')
    cfg.options.add_option('--mms-path', type=str, default=None, help='Chemin vers Metamod:Source')
    cfg.options.add_option('--sm-path', type=str, default=None, help='Chemin vers SourceMod')
    cfg.options.add_option('--enable-debug', action='store_const', const='1', dest='debug', help='Activer le mode debug')
    cfg.options.add_option('--enable-optimize', action='store_const', const='1', dest='opt', help='Activer les optimisations')
    cfg.options.add_option('--no-color', action='store_false', default=True, dest='color', help='Désactiver la sortie colorée')
    cfg.options.add_option('--disable-auto-versioning', action='store_true', default=False, dest='disable_auto_versioning', help='Désactiver la génération automatique de version')

    binary = cfg.Configure()

    # Configurer les options
    binary.sdks = util.FlagsParser().parse(getattr(binary.options, 'sdks', ''))
    binary.hl2sdk_root = binary.options.hl2sdk_root
    binary.mms_path = binary.options.mms_path
    binary.sm_path = binary.options.sm_path
    binary.debug = binary.options.debug
    binary.opt = binary.options.opt
    binary.color = binary.options.color
    binary.disable_auto_versioning = binary.options.disable_auto_versioning

    # Configurer les chemins par défaut si non spécifiés
    if not binary.hl2sdk_root:
        binary.hl2sdk_root = os.path.join('..', 'hl2sdk-css')
    if not binary.mms_path:
        binary.mms_path = os.path.join('..', 'metamod-source')
    if not binary.sm_path:
        binary.sm_path = os.path.join('..', 'sourcemod')

    # Vérifier si CSS est dans la liste des SDKs
    if 'all' in binary.sdks:
        binary.sdks = ['css']
    elif 'css' not in binary.sdks:
        binary.sdks = ['css']

    # Définir les options de compilation
    binary.compiler.cflags += ['-Wno-error', '-Wno-unknown-pragmas', '-Wno-dangling-else']
    binary.compiler.defines += ['_LINUX', 'PLATFORM_POSIX=1', 'PLATFORM_LINUX=1']

    # Générer le script de build
    binary.script_path = os.path.join(binary.build_root, 'AMBuildScript')

    # Exécuter le script de build
    binary.Generate(os.path.join(os.path.dirname(__file__), 'AMBuildScript'))

if __name__ == '__main__':
    run_configure(sys.argv)