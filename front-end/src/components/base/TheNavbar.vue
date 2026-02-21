<script setup>
// Theme
import { ref, onMounted, watch, computed } from 'vue';

const savedTheme = sessionStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const theme = ref(savedTheme || (prefersDark ? 'dark' : 'light'));
const isLightTheme = computed(() => theme.value === 'light');

const toggleTheme = () => {
	theme.value = theme.value === 'light' ? 'dark' : 'light';
};

watch(theme, (newTheme) => {
	document.documentElement.setAttribute('data-theme', newTheme);
	sessionStorage.setItem('theme', newTheme);
});

onMounted(() => {
	document.documentElement.setAttribute('data-theme', theme.value);
});

// Tabs
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useActiveTabStore } from '@/stores/activeTab';
import { useCurrentUserStore } from '@/stores/currentUser';

const router = useRouter();
const activeTabStore = useActiveTabStore();
const currentUserStore = useCurrentUserStore();
const { currentUser } = storeToRefs(currentUserStore);

const isActiveTab = (tab) => activeTabStore.activeTab === tab;

const tabs = [
	{ name: 'Landing', label: 'خانه' },
	{ name: 'DoctorsList', label: 'جستجوی پزشکان' },
];

// Mobile menu
const isMenuOpen = ref(false);

const openMenu = () => {
	isMenuOpen.value = true;
};

const closeMenu = () => {
	isMenuOpen.value = false;
};

const logout = () => {
	router.push({ name: 'Login' });
	currentUserStore.removeCurrentUser();
	closeMenu();
};
</script>

<template>
	<nav class="navbar">
		<div class="navbar__container">
			<router-link class="navbar__brand brand" :to="{ name: 'Landing' }">
				<h1 class="brand__text">CLINIX</h1>
			</router-link>
			<div class="navbar__burger burger" @click="openMenu">
				<SvgLoader class="burger__icon" name="burger-menu" />
			</div>
			<ul class="navbar__menu menu">
				<li v-for="(tab, index) in tabs" :key="index" class="menu__item">
					<h4 v-if="index > 0" class="menu__divider">|</h4>
					<router-link :to="{ name: tab.name }" class="menu__tab"
						:class="{ 'menu__tab--active': isActiveTab(tab.name) }">
						{{ tab.label }}
					</router-link>
				</li>
			</ul>
			<section class="navbar__buttons buttons">
				<SvgLoader class="buttons__theme-icon" :name="isLightTheme ? 'moon' : 'sun'" @click="toggleTheme" />
				<TheButton v-if="!currentUser" class="buttons__button" type="cancel" label="ثبت نام"
					@click="router.push({ name: 'Register' })" />
				<TheButton v-if="!currentUser" class="buttons__button" type="submit" label="ورود"
					@click="router.push({ name: 'Login' })" />
				<TheButton v-if="currentUser" class="buttons__button" type="cancel" label="مشاهده پروفایل"
					@click="router.push({ name: 'Notifications' })" />
				<TheButton v-if="currentUser" class="buttons__button buttons__exit" type="submit" label="خروج"
					@click="logout" />
			</section>
		</div>
	</nav>

	<transition name="slide">
		<div v-if="isMenuOpen" class="mobile-sidebar">
			<div class="mobile-sidebar__overlay" @click="closeMenu"></div>
			<div class="mobile-sidebar__content">
				<div class="mobile-sidebar__header">
					<TheButton label="بستن منو" type="hollow" @click="closeMenu" />
				</div>
				<ul class="mobile-sidebar__menu">
					<li v-for="(tab, index) in tabs" :key="index" class="mobile-sidebar__item">
						<router-link :to="{ name: tab.name }" class="mobile-sidebar__link"
							:class="{ 'mobile-sidebar__link--active': isActiveTab(tab.name) }" @click="closeMenu">
							{{ tab.label }}
						</router-link>
					</li>
				</ul>
				<div class="mobile-sidebar__buttons buttons">
					<SvgLoader class="buttons__theme-icon" :name="isLightTheme ? 'moon' : 'sun'" @click="toggleTheme" />
					<TheButton v-if="!currentUser" class="buttons__button" type="cancel" label="ثبت نام"
						@click="router.push({ name: 'Register' })" />
					<TheButton v-if="!currentUser" class="buttons__button" type="submit" label="ورود"
						@click="router.push({ name: 'Login' })" />
					<TheButton v-if="currentUser" class="buttons__button" type="cancel" label="مشاهده پروفایل"
						@click="router.push({ name: 'Notifications' })" />
					<TheButton v-if="currentUser" class="buttons__button buttons__exit" type="submit" label="خروج"
						@click="logout" />
				</div>
			</div>
		</div>
	</transition>
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
		width: $xl;
		@include flexbox(row, space-between, center, space(0), nowrap);
	}

	.brand {
		background-color: var(--primary-500);
		width: space(100);
		height: space(32);
		transition: all 0.4s ease;
		@include flexbox();

		&:hover {
			background-color: var(--primary-100);
		}

		&__text {
			color: var(--text-900);
		}
	}

	.burger {
		height: space(20);
		margin-left: space(6);

		@media (min-width: $md) {
			display: none;
		}

		&__icon {
			cursor: pointer;
			color: var(--text-900);
		}
	}

	.menu {
		height: space(20);
		@include flexbox(column, center, center, space(5));

		@media (max-width: $md) {
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
			transition: all 0.5s ease;
			padding-inline: space(4);
			border-top-left-radius: space(3);
			border-top-right-radius: space(3);
			border-bottom: space(1) solid transparent;
			@include flexbox();

			&:hover {
				background-color: var(--primary-600);
			}

			&--active {
				border-bottom: space(1) solid var(--title-100);
			}
		}
	}

	.buttons {
		@include flexbox(row, space-between, center, space(6), nowrap);

		@media (max-width: $xl) {
			padding-inline: space(6);
		}

		@media (max-width: $md) {
			display: none;
		}

		&__theme-icon {
			color: var(--text-700);
			cursor: pointer;
			padding: space(3);
			border-radius: space(3);
			transition: all 0.4s ease;

			&:hover {
				background: var(--bg-500);
			}
		}

		&__button {
			width: space(50);
		}

		&__exit {
			background-color: var(--red-300);

			&:hover {
				background-color: var(--red-500);
			}
		}
	}
}

.mobile-sidebar {
	position: fixed;
	inset: 0;
	z-index: 1000;
	pointer-events: none;

	&__overlay {
		position: absolute;
		inset: 0;
		background: rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(2px);
		pointer-events: auto;
	}

	&__content {
		position: absolute;
		top: space(0);
		bottom: space(0);
		left: space(0);
		width: 80vw;
		max-width: space(160);
		background-color: var(--bg-800);
		pointer-events: auto;
		display: flex;
		flex-direction: column;
	}

	&__header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: space(6) space(6) space(4);
		border-bottom: 1px solid var(--text-200);
	}

	&__menu {
		flex: 1;
		padding: space(4) 0;
		list-style: none;
	}

	&__item {
		padding: 0 space(6);
		margin-bottom: space(9);
	}

	&__link {
		display: block;
		padding: space(5) space(4);
		color: var(--title-900);
		font-size: 1.1rem;
		border-radius: space(3);
		background: var(--primary-600);
		transition: all 0.4s;

		&:hover,
		&--active {
			background: var(--primary-100);
			color: white;
		}
	}

	.buttons {
		padding: space(6);
		border-top: 1px solid var(--text-200);
		display: flex;
		align-items: center;
		flex-direction: column;
		gap: space(5);

		&__theme-icon {
			color: var(--text-700);
			cursor: pointer;
			padding: space(4);
			border-radius: space(3);
			transition: all 0.4s ease;

			&:hover {
				background: var(--bg-700);
			}
		}

		&__exit {
			background-color: var(--red-300);

			&:hover {
				background-color: var(--red-500);
			}
		}
	}
}
</style>
