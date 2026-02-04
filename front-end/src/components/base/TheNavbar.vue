<script setup>
	// Theme
	import { ref, onMounted, watch, computed } from 'vue';

	const savedTheme = localStorage.getItem('theme');
	const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
	const theme = ref(savedTheme || (prefersDark ? 'dark' : 'light'));
	const isLightTheme = computed(() => theme.value === 'light');

	const toggleTheme = () => {
		theme.value = theme.value === 'light' ? 'dark' : 'light';
	};

	watch(theme, (newTheme) => {
		document.documentElement.setAttribute('data-theme', newTheme);
		localStorage.setItem('theme', newTheme);
	});

	onMounted(() => {
		document.documentElement.setAttribute('data-theme', theme.value);
	});

	// Tabs
	import { useActiveTabStore } from '@/stores/activeTab';
	import { useRouter } from 'vue-router';

	const router = useRouter();
	const activeTabStore = useActiveTabStore();

	const setActiveTab = (tab) => activeTabStore.setActiveTab(tab);

	const isActiveTab = (tab) => activeTabStore.activeTab === tab;

	const tabs = [
		{ name: 'Home', label: 'مطالب' },
		{ name: 'Profile', label: 'درباره ما' },
		{ name: 'Register', label: 'ثبت نام' },
		{ name: 'Login', label: 'دیتای ماک شده' },
	];
</script>

<template>
	<nav class="navbar">
		<div class="navbar__container">
			<router-link
				class="navbar__brand brand"
				:to="{ name: 'Home' }"
				@click="setActiveTab('')"
			>
				<img class="brand__image" v-if="isLightTheme" src="/navicon-dark.png" />
				<img class="brand__image" v-else src="/navicon-light.png" />
			</router-link>
			<ul class="navbar__menu menu">
				<li v-for="(tab, index) in tabs" :key="index" class="menu__item">
					<h4 v-if="index > 0" class="menu__divider">|</h4>
					<router-link
						@click="setActiveTab(tab.name)"
						:to="{ name: tab.name }"
						class="menu__tab"
						:class="{ 'menu__tab--active': isActiveTab(tab.name) }"
					>
						{{ tab.label }}
					</router-link>
				</li>
			</ul>
			<section class="navbar__buttons buttons">
				<TheButton
					@click="toggleTheme"
					type="hollow"
					:label="isLightTheme ? 'تاریک' : 'روشن'"
				/>
				<TheButton
					type="submit"
					label="ورود"
					@click="router.push({ name: 'Login' })"
				/>
				<TheButton
					type="cancel"
					label="ثبت نام"
					@click="router.push({ name: 'Register' })"
				/>
			</section>
		</div>
	</nav>
</template>

<style lang="scss" scoped>
	.navbar {
		position: fixed;
		top: space(0);
		background-color: var(--bg-900);
		box-shadow: space(0) space(2) space(4) var(--text-100);
		width: 100%;
		height: space(32);
		z-index: 1;
		@include flexbox();

		&__container {
			width: space(650);
			@include flexbox(row, space-between);
			@media (max-width: space(300)) {
				@include flexbox();
			}
		}

		.brand {
			&__image {
				width: space(100);
				height: space(32);
				@include flexbox();
			}
		}

		.menu {
			height: space(20);
			@include flexbox(column, center, center, space(5));
			@media (max-width: space(450)) {
				display: none;
			}

			&__item {
				height: 100%;
				@include flexbox(column, center, center, space(5));
			}

			&__divider {
				color: var(--text-100);
				user-select: none;
			}

			&__tab {
				height: 100%;
				color: var(--title-500);
				padding-inline: space(4);
				border-bottom: space(1) solid transparent;
				@include flexbox();

				&:hover {
					background-color: var(--primary-800);
				}

				&--active {
					border-bottom: space(1) solid var(--title-100);
				}
			}
		}

		.buttons {
			padding-inline: space(5);
			width: space(120);
			@include flexbox(row, center, center, space(8), nowrap);
			@media (max-width: space(300)) {
				display: none;
			}
		}
	}
</style>
