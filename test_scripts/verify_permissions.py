import os
import sys

if __name__ == "__main__":
    # Obtenemos la ruta absoluta donde está este script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # La raíz del proyecto está un nivel arriba de 'test_scripts'
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from database.sync.verify_permissions import main
    main()
