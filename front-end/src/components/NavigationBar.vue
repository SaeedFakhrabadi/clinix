<script setup>
	// Theme
	import { ref, onMounted, watch } from 'vue';

	const savedTheme = localStorage.getItem('theme');
	const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
	const theme = ref(savedTheme || (prefersDark ? 'dark' : 'light'));
	const isLightImage = computed(() => theme.value === 'light');

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
	import { computed } from 'vue';

	const router = useRouter();

	const activeTabStore = useActiveTabStore();

	const setActiveTab = (tab) => activeTabStore.setActiveTab(tab);

	const isActiveTab = (tab) => activeTabStore.activeTab === tab;

	const tabs = [
		{ name: 'Home', label: 'مطالب' },
		{ name: 'Home', label: 'درباره ما' },
	];
</script>

<template>
	<nav class="navigation-bar">
		<div class="navigation-bar__container">
			<router-link :to="{ name: 'Home' }" @click="setActiveTab('')">
				<img v-if="isLightImage" class="navigation-bar__image" src="./../../public/navicon.png" />
				<img v-else class="navigation-bar__image" src="./../../public/navicon-hover.png" />
			</router-link>
			<div class="navigation-bar__menu">
				<router-link
					v-for="tab in tabs"
					:key="tab.name"
					:to="{ name: tab.name }"
					@click="setActiveTab(tab.name)"
				>
					<h4
						class="navigation-bar__menu-tab"
						:class="{
							'navigation-bar__menu-tab--active': isActiveTab(tab.name),
						}"
					>
						{{ tab.label }}
					</h4>
				</router-link>
			</div>
			<div class="navigation-bar__buttons">
				<TheButton
					@click="toggleTheme"
					type="hollow"
					:label="theme === 'light' ? 'تاریک' : 'روشن'"
				/>
				<TheButton type="submit" label="ورود" @click="router.push({ name: 'Login' })" />
				<TheButton type="cancel" label="ثبت نام" @click="router.push({ name: 'SignUp' })" />
			</div>
		</div>
	</nav>
</template>

<style lang="scss" scoped>
	.navigation-bar {
		position: sticky;
		top: space(0);
		padding: space(0) 15%;
		background-color: var(--bg-900);
		box-shadow: space(0) space(2) space(4) var(--text-100);
		z-index: 10;
		@include flexbox();

		&__container {
			width: space(550);
			@include flexbox(row, space-between);
			@media (max-width: space(300)) {
				@include flexbox();
			}
		}

		&__image {
			width: space(100);
			@include flexbox();
		}

		&__menu {
			@include flexbox();
			@media (max-width: space(610)) {
				display: none;
			}
		}

		&__menu-tab {
			color: var(--title-500);
			text-shadow: space(0) space(1) space(15) var(--title-500);
			padding: space(1) space(4);
			border: space(1) solid transparent;

			&:hover {
				color: var(--primary-400);
			}

			&--active {
				color: var(--primary-400);
				border-bottom: space(1) solid var(--title-100);
			}
		}

		&__buttons {
			width: space(120);
			@include flexbox(row, center, center, space(8), nowrap);
			@media (max-width: space(300)) {
				display: none;
			}
		}
	}
</style>
