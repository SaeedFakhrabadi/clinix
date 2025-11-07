export default {
	path: '/home',
	name: 'Home',
	component: () => import('@/layouts/Home.vue'),
	redirect: '/home/landing',
	children: [
		{
			path: 'landing',
			name: 'Landing',
			component: () => import('@/views/home/Landing.vue'),
		},
	],
};
