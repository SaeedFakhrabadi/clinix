export default {
	path: '/auth',
	name: 'Auth',
	component: () => import('@/layouts/Auth.vue'),
	redirect: '/auth/login',
	children: [
		{
			path: 'login',
			name: 'Login',
			component: () => import('@/views/auth/Login.vue'),
		},
		{
			path: 'register',
			name: 'Register',
			component: () => import('@/views/auth/Register.vue'),
		},
		{
			path: 'recovery-password',
			name: 'RecoveryPassword',
			component: () => import('@/views/auth/RecoveryPassword.vue'),
		},
		{
			path: 'change-password',
			name: 'ChangePassword',
			component: () => import('@/views/auth/ChangePassword.vue'),
		},
	],
};
