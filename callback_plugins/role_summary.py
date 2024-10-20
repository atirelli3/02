from ansible.plugins.callback import CallbackBase
import sys

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'role_summary'

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.role_results = {}

    def v2_playbook_on_task_start(self, task, is_conditional):
        role_name = task._role.get_name() if task._role else 'No Role'
        task_name = task.get_name()
        
        if role_name not in self.role_results:
            self.role_results[role_name] = []
        
        self.role_results[role_name].append({'task': task_name, 'status': None})

    def v2_runner_on_ok(self, result):
        role_name = result._task._role.get_name() if result._task._role else 'No Role'
        task_name = result._task.get_name()
        self._update_task_status(role_name, task_name, 'ok')

    def v2_runner_on_failed(self, result, ignore_errors=False):
        role_name = result._task._role.get_name() if result._task._role else 'No Role'
        task_name = result._task.get_name()
        self._update_task_status(role_name, task_name, 'failed')

    def v2_runner_on_skipped(self, result):
        role_name = result._task._role.get_name() if result._task._role else 'No Role'
        task_name = result._task.get_name()
        self._update_task_status(role_name, task_name, 'skipped')

    def v2_playbook_on_stats(self, stats):
        print("\nTASK SUMMARY BY ROLE:")
        for role, tasks in self.role_results.items():
            print(f"\nROLE [{role.upper()}] ****************************************************")
            for task in tasks:
                status = task['status']
                status_color = self._get_color_for_status(status)
                print(f"    - {task['task']}: {status_color}{status}\033[0m")

    def _update_task_status(self, role, task_name, status):
        for task in self.role_results[role]:
            if task['task'] == task_name:
                task['status'] = status
                break

    def _get_color_for_status(self, status):
        if status == 'ok':
            return "\033[92m"  # Green
        elif status == 'failed':
            return "\033[91m"  # Red
        elif status == 'skipped':
            return "\033[93m"  # Yellow
        return ""
