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
	<aside class="the-sidebar">
		<header class="the-sidebar__header header">
			<!-- <TheIcon class="header__profile" name="profile-circle" /> -->
			<img class="header__profile" src="/doctor.png" />
			<hr class="header__divider" />
			<div class="header__user-info">
				<h4 class="header__user-name">
					{{ currentUserStore?.currentUser?.name }}
				</h4>
				<h4 class="header__user-role">
					{{ currentUserStore?.currentUser?.role?.label }}
				</h4>
			</div>
		</header>
		<hr class="the-sidebar__divider" />
		<div class="the-sidebar__content">
			<ul class="the-sidebar__menu menu">
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
				</li>
			</ul>
			<TheButton
				class="the-sidebar__exit"
				label="خروج"
				type="submit"
				icon-name="logout"
				@click="logout"
			/>
		</div>
	</aside>
</template>

<style lang="scss" scoped>
	.the-sidebar {
		background-color: var(--bg-900);
		width: space(150);
		padding: space(8) space(6) space(6) space(6);
		height: 100%;
		box-sizing: border-box;
		@include flexbox(column, start, center, space(8), nowrap);

		@media (max-width: $lg) {
			width: space(110);
		}

		@media (max-width: $md) {
			display: none;
		}

		.header {
			width: 100%;
			padding: space(6);
			box-sizing: border-box;
			border-radius: space(6);
			background-color: var(--primary-700);
			@include flexbox(row, center, center, space(6), nowrap);

			&__profile {
				width: space(40);
				height: space(40);
				border-radius: 50%;
				object-fit: cover;
				color: var(--text-900);
			}

			&__divider {
				height: 100%;
				border-right: space(0.5) solid var(--text-900);
			}

			&__user-info {
				flex: 1;
				color: var(--text-900);
				@include flexbox(column, center, start, space(2));
			}

			&__user-name {
				@include lineClamp(2);
			}

			&__user-role {
				color: var(--title-300);
			}
		}

		&__divider {
			width: 100%;
			border-top: space(0.5) solid var(--text-900);
		}

		&__content {
			width: 100%;
			flex: 1;
			overflow: auto;
			@include flexbox(column, space-between, start, space(0), nowrap);
		}

		.menu {
			width: 100%;
			flex: 1;
			@include flexbox(column, start, center, space(6), nowrap);

			&__item {
				width: 100%;
				@include flexbox(column, center, center, space(0));
			}

			&__tab {
				width: 100%;
				height: space(25);
				background-color: var(--bg-700);
				border-radius: space(6);
				color: var(--text-900);
				transition: all 0.5s ease;
				@include flexbox(row, center, center, space(0));

				&:hover {
					background-color: var(--primary-400);
				}

				&--active {
					color: var(--title-100);
					background-color: var(--primary-600);
				}
			}
		}

		&__exit {
			margin-top: space(6);
			background-color: var(--red-100);
			color: var(--text-900);
			min-height: space(25);

			&:hover {
				background-color: var(--red-300);
			}
		}
	}
</style>
