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

	const closeNotification = (id) => {
		notifications.value = notifications.value.filter((n) => n?.id !== id);
		// const data = deleteNotification()
	};

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
						n?.notification_type === 'RESERVE'
							? 'notifications__item--reserve'
							: 'notifications__item--cancel'
					"
				>
					<p class="notifications__message">
						{{ toPersianDigits(n?.message) }}
					</p>
					<h2 class="notifications__delete" @click="closeNotification(n?.id)">
						&times;
					</h2>
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
			@include flexbox(column, center, start, space(6), nowrap);
		}

		&__list {
			width: 100%;
			list-style: none;
			padding: space(0);
			margin: space(0);
			@include flexbox(column, center, center, space(6), nowrap);
		}

		&__item {
			width: 100%;
			border-radius: space(6);
			box-sizing: border-box;
			padding: space(5);
			@include flexbox(row, space-between, center, space(0), nowrap);

			&--reserve {
				color: var(--success-600);
				background-color: var(--green-600);
			}

			&--cancel {
				color: var(--danger-600);
				background-color: var(--red-600);
			}
		}

		&__delete {
			cursor: pointer;
			line-height: space(16);
			user-select: none;
			padding-inline: space(4);
		}
	}
</style>
