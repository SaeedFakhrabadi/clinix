<script setup>
	import { onMounted, ref } from 'vue';
	import { useToast } from 'vue-toastification';
	import { storeToRefs } from 'pinia';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import { getNotifications } from '@/services/notifications';

	const toast = useToast();

	const notifications = ref(null);
	const loading = ref(true);
	const empty = ref(false);

	const currentUserStore = useCurrentUserStore();
	const { currentUser } = storeToRefs(currentUserStore);

	onMounted(async () => {
		loading.value = true;
		try {
			const response = await getNotifications(currentUser.value);
			notifications.value = response?.data?.notifications;
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');

			notifications.value = [];
			empty.value = true;
		} finally {
			loading.value = false;
		}
	});
</script>

<template>
	<div class="notifications">
		<div v-if="loading" class="notifications__state--loading">
			<h2>در حال دریافت اعلان ها...</h2>
		</div>
		<div v-else-if="empty" class="notifications__state--empty">
			<h2>خطا در دریافت اعلان ها!</h2>
		</div>
		<div v-else-if="notifications?.length" class="notifications__container">
			<h2 class="notifications__title">لیست اعلان ها</h2>
			<ul class="notifications__list">
				<li
					v-for="(n, index) in notifications"
					:key="index"
					class="notifications__item"
					:class="
						n.notification_type === 'RESERVE'
							? 'notifications__item--reserve'
							: 'notifications__item--cancel'
					"
				>
					<p class="notifications__message">{{ toPersianDigits(n.message) }}</p>
				</li>
			</ul>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.notifications {
		padding-left: space(6);
		width: 100%;
		@include flexbox(column, center, center, space(14), nowrap);

		&__state {
			&--loading {
				color: var(--text-500);
			}
			&--empty {
				color: var(--danger-500);
			}
		}

		&__container {
			width: 100%;
			@include flexbox(column, center, start, space(14), nowrap);
		}

		&__title {
			color: var(--text-900);
			padding-right: space(4);
			border-right: space(4) solid var(--title-100);
		}

		&__list {
			width: 100%;
			list-style: none;
			padding: space(0);
			margin: space(0);
			@include flexbox(column, center, center, space(6), nowrap);
		}

		&__item {
			width: calc(100% - space(12));
			border-radius: space(6);
			padding: space(5);

			&--reserve {
				border: space(1) solid var(--green-100);
				background-color: var(--green-700);
			}

			&--cancel {
				border: space(1) solid var(--red-100);
				background-color: var(--red-700);
			}
		}

		&__message {
			color: var(--text-600);
		}
	}
</style>
