from os.path import join as path_join

from backend_app.settings import BASE_DIR


templates_dir = path_join(BASE_DIR, "templates")
templates_to_load_paths = {
    'emails/user-invites/complete.txt': path_join(templates_dir, 'emails', 'user-invites', 'complete.txt'),
    'emails/user-invites/no_sender.txt': path_join(templates_dir, 'emails', 'user-invites', 'no_sender.txt'),
    'emails/user-invites/no_receiver.txt': path_join(templates_dir, 'emails', 'user-invites', 'no_receiver.txt'),
    'emails/user-invites/no_sender_no_receiver.txt': path_join(templates_dir, 'emails', 'user-invites', 'no_sender_no_receiver.txt'),
    'emails/user-invites/complete.html': path_join(templates_dir, 'emails', 'user-invites', 'complete.html'),
    'emails/user-invites/no_sender.html': path_join(templates_dir, 'emails', 'user-invites', 'no_sender.html'),
    'emails/user-invites/no_receiver.html': path_join(templates_dir, 'emails', 'user-invites', 'no_receiver.html'),
    'emails/user-invites/no_sender_no_receiver.html': path_join(templates_dir, 'emails', 'user-invites', 'no_sender_no_receiver.html'),
}


def load_templates():
    loaded_templates = {}

    for template_name, template_path in templates_to_load_paths.items():
        with open(template_path, 'r', encoding="utf-8") as template_file:
            template_content = template_file.read()

        loaded_templates[template_name] = template_content

    return loaded_templates
