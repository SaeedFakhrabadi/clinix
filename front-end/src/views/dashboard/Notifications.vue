<script setup>
	import { onMounted, ref } from 'vue';
	import { useToast } from 'vue-toastification';
	import { useRouter } from 'vue-router';
	import { storeToRefs } from 'pinia';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import { getNotifications } from '@/services/notifications';

	const router = useRouter();
	const toast = useToast();

	const notifications = ref(null);
	const loading = ref(true);
	const loadingError = ref(null);

	const currentUserStore = useCurrentUserStore();
	const { currentUser } = storeToRefs(currentUserStore);

	onMounted(async () => {
		loading.value = true;
		try {
			const response = await getNotifications(currentUser.value);
			notifications.value = response?.data?.notifications;

			loading.value = false;
		} catch (error) {
			if (
				error?.response?.data?.detail ===
				'Authentication credentials were not provided.'
			) {
				toast.error('!زمان ورود شما منقضی شده است، لطفا دوباره وارد شوید');
				currentUserStore.removeCurrentUser();
				router.push({ name: 'Login' });
				return;
			}

			console.error('Error : ', error?.response?.data || error?.message);

			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');

			loading.value = false;
			loadingError.value = true;
		}
	});
</script>

<template>
	<div class="notifications">
		<div v-if="loading" class="notifications__state--loading">
			<h2>در حال دریافت اعلان ها...</h2>
		</div>
		<div v-else-if="loadingError" class="notifications__state--error">
			<h2>خطا در دریافت اعلان ها!</h2>
		</div>
		<div v-else-if="notifications?.length" class="notifications__container">
			<TheTitle label="لیست اعلان ها" />
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
		<div v-else class="notifications__state--empty">
			<h2>در حال حاضر اعلانی وجود ندارد!</h2>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.notifications {
		&__state {
			&--loading {
				color: var(--text-500);
			}
			&--error {
				color: var(--danger-500);
			}
			&--empty {
				color: var(--text-500);
			}
		}

		&__container {
			width: 100%;
			@include flexbox(column, center, start, space(14), nowrap);
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
