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
			path: 'sign-up',
			name: 'SignUp',
			component: () => import('@/views/auth/SignUp.vue'),
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
