#!/usr/bin/env python
import sys
import os

try:
    from ambuild2 import run
    from ambuild2.frontend import app_main
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
    # Utiliser l'API app_main pour configurer le build
    app = app_main.App(args)
    
    # Ajouter les options de ligne de commande
    app.add_argument('--sdks', type=str, default='all', help='Liste des SDKs à utiliser (all, css, tf2, l4d2, etc.)')
    app.add_argument('--hl2sdk-root', type=str, default=None, help='Chemin racine pour les HL2SDKs')
    app.add_argument('--mms-path', type=str, default=None, help='Chemin vers Metamod:Source')
    app.add_argument('--sm-path', type=str, default=None, help='Chemin vers SourceMod')
    app.add_argument('--enable-debug', action='store_const', const='1', dest='debug', help='Activer le mode debug')
    app.add_argument('--enable-optimize', action='store_const', const='1', dest='opt', help='Activer les optimisations')
    app.add_argument('--no-color', action='store_false', default=True, dest='color', help='Désactiver la sortie colorée')
    app.add_argument('--disable-auto-versioning', action='store_true', default=False, dest='disable_auto_versioning', help='Désactiver la génération automatique de version')
    
    # Configurer le build
    app.configure_logging()
    app.default_build_folder = make_objdir_name
    
    # Exécuter la configuration
    builder = app.create_build_objects()
    builder.options.sdks = getattr(app.args, 'sdks', 'all').split(',')
    builder.options.hl2sdk_root = app.args.hl2sdk_root
    builder.options.mms_path = app.args.mms_path
    builder.options.sm_path = app.args.sm_path
    builder.options.debug = app.args.debug
    builder.options.opt = app.args.opt
    builder.options.color = app.args.color
    builder.options.disable_auto_versioning = app.args.disable_auto_versioning
    
    # Configurer les chemins par défaut si non spécifiés
    if not builder.options.hl2sdk_root:
        builder.options.hl2sdk_root = os.path.join('..', 'hl2sdk-css')
    if not builder.options.mms_path:
        builder.options.mms_path = os.path.join('..', 'metamod-source')
    if not builder.options.sm_path:
        builder.options.sm_path = os.path.join('..', 'sourcemod')
    
    # Vérifier si CSS est dans la liste des SDKs
    if 'all' in builder.options.sdks:
        builder.options.sdks = ['css']
    elif 'css' not in builder.options.sdks:
        builder.options.sdks = ['css']
    
    # Générer le script de build
    app.generate(builder, os.path.join(os.path.dirname(__file__), 'AMBuildScript'))

if __name__ == '__main__':
    run_configure(sys.argv)