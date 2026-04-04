import { reactive } from 'vue'

export const authStore = reactive({
    accessToken: localStorage.getItem('access_token') || null,
    userRole: localStorage.getItem('user_role') || null,
    username: localStorage.getItem('username') || null,
    isAuthenticated: !!localStorage.getItem('access_token'),

    setAuth(access, role, username) {
        this.accessToken = access;
        this.userRole = role;
        this.username = username;
        this.isAuthenticated = true;
        localStorage.setItem('access_token', access);
        localStorage.setItem('user_role', role);
        localStorage.setItem('username', username);
    },

    logout() {
        this.accessToken = null;
        this.userRole = null;
        this.username = null;
        this.isAuthenticated = false;
        localStorage.clear();
    }
});
