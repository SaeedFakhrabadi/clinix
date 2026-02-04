<script setup>
	import { defineProps } from 'vue';
	import { useRouter } from 'vue-router';
	import { useActiveTabStore } from '@/stores/activeTab';

	const props = defineProps({
		items: { type: Array },
	});

	const router = useRouter();
	const activeTabStore = useActiveTabStore();

	const setActiveTab = (tab) => activeTabStore.setActiveTab(tab);

	const isActiveTab = (tab) => activeTabStore.activeTab === tab;

	const logout = () => {
		router.push({ name: 'Login' });
	};
</script>

<template>
	<aside class="sidebar">
		<header class="sidebar__header header">
			<SvgLoader class="header__profile" name="profile-circle" />
			<h4 class="header__name">محمد سعید فخرآبادی</h4>
		</header>
		<ul class="sidebar__menu menu">
			<li v-for="(item, index) in props.items" :key="index" class="menu__item">
				<hr v-if="index > 0" class="menu__divider" />
				<router-link
					class="menu__tab"
					:class="{ 'menu__tab--active': isActiveTab(item.name) }"
					@click="setActiveTab(item.name)"
					:to="{ name: item.name }"
				>
					{{ item.label }}
				</router-link>
			</li>
			<TheButton label="خروج" type="cancel" @click="logout" />
		</ul>
	</aside>
</template>

<style lang="scss" scoped>
	.sidebar {
		background-color: var(--bg-900);
		width: space(150);
		height: 100%;
		border-left: space(1) solid var(--primary-500);
		transition: none;
		@include flexbox(column, start, center);

		.header {
			width: 90%;
			height: space(100);
			color: white;
			border-bottom: space(1) solid var(--text-100);
			@include flexbox(column, center, center, space(0));

			&__profile {
				width: space(50);
				height: space(50);
			}

			&__name {
				color: var(--text-900);
			}
		}

		.menu {
			width: 90%;
			height: space(200);
			overflow: auto;
			@include flexbox(column, start, center, space(0), nowrap);

			&__item {
				width: 100%;
				@include flexbox(column, center, center, space(0));
			}

			&__tab {
				width: calc(100% - space(8));
				height: space(30);
				border-right: space(5) solid transparent;
				padding-right: space(3);
				color: var(--title-500);
				cursor: pointer;
				@include flexbox(row, start, center, space(0));

				&:hover {
					background-color: var(--primary-800);
				}

				&--active {
					border-right: space(5) solid var(--title-100);
				}
			}

			&__divider {
				width: 100%;
				border: none;
				border-top: space(0.5) solid var(--text-100);
			}
		}
	}
</style>
