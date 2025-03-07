#!/usr/bin/env python
import sys
try:
    from ambuild2 import run
except:
    try:
        import ambuild
        sys.stderr.write('AMBuild 1 is no longer supported. Please upgrade to AMBuild 2.\n')
    except:
        sys.stderr.write('AMBuild must be installed to build this project.\n')
    sys.exit(1)

# Fonction principale
def make_objdir_name(p):
    return 'obj-' + p.target_platform + '-' + p.target_arch

def run_configure(args):
    # Créer un parser d'arguments
    from ambuild2.frontend.v2_1.context import Context
    from ambuild2.frontend.v2_1.cpp.detect import Compiler
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('--sdks', type='string', dest='sdks', default='all', help='Liste des SDKs à utiliser (all, css, tf2, l4d2, etc.)')
    parser.add_option('--hl2sdk-root', type='string', dest='hl2sdk_root', default=None, help='Chemin racine pour les HL2SDKs')
    parser.add_option('--mms-path', type='string', dest='mms_path', default=None, help='Chemin vers Metamod:Source')
    parser.add_option('--sm-path', type='string', dest='sm_path', default=None, help='Chemin vers SourceMod')
    parser.add_option('--enable-debug', action='store_const', const='1', dest='debug', help='Activer le mode debug')
    parser.add_option('--enable-optimize', action='store_const', const='1', dest='opt', help='Activer les optimisations')
    parser.add_option('--no-color', action='store_false', default=True, dest='color', help='Désactiver la sortie colorée')
    parser.add_option('--disable-auto-versioning', action='store_true', default=False, dest='disable_auto_versioning', help='Désactiver la génération automatique de version')

    # Analyser les arguments
    options, args = parser.parse_args()

    # Créer le contexte de build
    context = Context(make_objdir_name)
    context.detect(Compiler)

    # Configurer les options
    context.options.sdks = options.sdks.split(',')
    context.options.hl2sdk_root = options.hl2sdk_root
    context.options.mms_path = options.mms_path
    context.options.sm_path = options.sm_path
    context.options.debug = options.debug
    context.options.opt = options.opt
    context.options.color = options.color
    context.options.disable_auto_versioning = options.disable_auto_versioning

    # Configurer les chemins par défaut si non spécifiés
    if not context.options.hl2sdk_root:
        context.options.hl2sdk_root = '../hl2sdk-css'
    if not context.options.mms_path:
        context.options.mms_path = '../metamod-source'
    if not context.options.sm_path:
        context.options.sm_path = '../sourcemod'

    # Vérifier si CSS est dans la liste des SDKs
    if 'all' in context.options.sdks:
        context.options.sdks = ['css']
    elif 'css' not in context.options.sdks:
        context.options.sdks = ['css']

    # Lancer le script de build
    run.generate(context, args)

if __name__ == '__main__':
    run_configure(sys.argv)