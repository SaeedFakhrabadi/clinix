<script setup>
	import { defineProps } from 'vue';
	import { useRouter } from 'vue-router';
	import { useActiveTabStore } from '@/stores/activeTab';
	import { useCurrentUserStore } from '@/stores/currentUser';

	const props = defineProps({
		items: { type: Array, required: true },
	});

	const router = useRouter();
	const activeTabStore = useActiveTabStore();
	const currentUserStore = useCurrentUserStore();

	const isActiveTab = (tab) => activeTabStore.activeTab === tab;

	const logout = () => {
		router.push({ name: 'Login' });
		currentUserStore.removeCurrentUser();
	};
</script>

<template>
	<aside class="sidebar">
		<header class="sidebar__header header">
			<SvgLoader class="header__profile" name="profile-circle" />
			<div class="header__user-info">
				<span style="color: var(--text-900)">
					{{ currentUserStore?.currentUser?.name }}
				</span>
				<span style="color: var(--text-100)">|</span>
				<span style="color: var(--title-300)"
					>{{ currentUserStore?.currentUser?.role?.label }}
				</span>
			</div>
		</header>
		<div class="sidebar__content">
			<ul class="sidebar__menu menu">
				<li
					v-for="(item, index) in props.items"
					:key="index"
					class="menu__item"
				>
					<router-link
						class="menu__tab"
						:class="{ 'menu__tab--active': isActiveTab(item?.name) }"
						:to="{ name: item?.name }"
					>
						{{ item?.label }}
					</router-link>
					<hr class="menu__divider" />
				</li>
			</ul>
			<TheButton
				class="sidebar__exit"
				label="خروج"
				type="cancel"
				icon-name="logout"
				@click="logout"
			/>
		</div>
	</aside>
</template>

<style lang="scss" scoped>
	.sidebar {
		background-color: var(--bg-900);
		width: space(180);
		height: 100%;
		border-left: space(1) solid var(--primary-500);
		transition: none;
		@include flexbox(column, start, center);
		@media (max-width: $lg) {
			width: space(150);
		}
		@media (max-width: $md) {
			width: space(120);
		}
		@media (max-width: $sm) {
			display: none;
		}

		.header {
			width: 90%;
			height: space(100);
			color: white;
			border-bottom: space(1) solid var(--text-100);
			@include flexbox(column, center, center, space(0));

			&__profile {
				width: space(50);
				height: space(50);
				color: var(--text-900);
			}

			&__user-info {
				width: 100%;
				color: var(--text-900);
				@include flexbox(row, center, center, space(4));
			}
		}

		&__content {
			width: 90%;
			flex: 1;
			padding-bottom: space(10);
			@include flexbox(column, space-between, start, space(0));
		}

		.menu {
			width: 100%;
			@include flexbox(column, start, center, space(0));

			&__item {
				width: 100%;
				@include flexbox(column, center, center, space(0));
			}

			&__divider {
				width: 100%;
				border: none;
				border-top: space(0.5) solid var(--text-100);
			}

			&__tab {
				width: calc(100% - space(10));
				height: space(30);
				border-right: space(5) solid transparent;
				padding-right: space(5);
				color: var(--title-500);
				transition: all 0.5s ease;
				cursor: pointer;
				@include flexbox(row, start, center, space(0));

				&:hover {
					background-color: var(--primary-600);
				}

				&--active {
					background-color: var(--primary-800);
					border-right: space(5) solid var(--title-100);
				}
			}
		}

		&__exit {
			background-color: var(--red-800);
			border: space(1) solid var(--red-100);
			color: var(--red-100);
			height: space(25);

			&:hover {
				background-color: var(--red-600);
			}
		}
	}
</style>
