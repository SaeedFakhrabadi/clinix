<script setup>
	import { computed, onMounted, ref } from 'vue';
	import { useRoute, useRouter } from 'vue-router';
	import { storeToRefs } from 'pinia';
	import { doctorDetails } from '@/services/doctors';
	import { createReservation } from '@/services/reservations';
	import { createTransaction } from '@/services/transactions';
	import { addCommas } from '@/utils/addCommas';
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import { useCurrentUserStore } from '@/stores/currentUser';

	const route = useRoute();
	const router = useRouter();

	const currentUserStore = useCurrentUserStore();
	const { currentUser } = storeToRefs(currentUserStore);

	const doctor = ref(null);
	const loading = ref(true);
	const error = ref(null);

	const did = computed(() => route.query.did);

	const pay = (data) => {
		// createTransaction(
		// 	data?.transactionData.value?.method,
		// 	data?.transactionData.value?.pid,
		// 	data?.transactionData.value?.price,
		// 	data?.transactionData.value?.type,
		// );

		// createReservation(
		// 	data?.reservationData.value?.did,
		// 	data?.reservationData.value?.pid,
		// 	data?.reservationData.value?.time,
		// );

		router.push({ name: 'Reservations' });
	};

	onMounted(async () => {
		loading.value = true;
		error.value = null;

		try {
			const { data } = await doctorDetails(did.value);
			doctor.value = data;
		} catch (e) {
			error.value = 'دریافت اطلاعات پزشک با خطا مواجه شد.';
			console.error(e);
		} finally {
			loading.value = false;
		}
	});
</script>

<template>
	<div class="doctor-details">
		<div v-if="loading" class="doctor-details__state--loading">
			<h2>در حال دریافت اطلاعات پزشک...</h2>
		</div>
		<div v-else-if="error" class="doctor-details__state--error">
			<h2>خطا در دریافت اطلاعات پزشک!</h2>
		</div>
		<div v-else-if="doctor" class="doctor-details__container">
			<section class="doctor-details__comments">
				<h2 class="doctor-details__section-title">نظرات کاربران</h2>
				<ul v-if="doctor?.comments?.length" class="comments-list">
					<li
						v-for="(c, i) in doctor?.comments"
						:key="i"
						class="comments-list__item comment"
					>
						<div class="comment__meta">
							<span class="comment__user">{{ c.username }}</span>
							<span class="comment__score"
								>امتیاز: {{ toPersianDigits(c.score) }}/۵</span
							>
						</div>
						<p class="comment__text">{{ c.comment }}</p>
					</li>
				</ul>
				<p v-else class="doctor-details__empty">هنوز نظری ثبت نشده است.</p>
			</section>
			<ScheduleTable :doctor="doctor" :currentUser="currentUser" @pay="pay" />
			<section class="doctor-details__comments">
				<h2 class="doctor-details__section-title">نظرات کاربران</h2>
				<ul v-if="doctor?.comments?.length" class="comments-list">
					<li
						v-for="(c, i) in doctor?.comments"
						:key="i"
						class="comments-list__item comment"
					>
						<div class="comment__meta">
							<span class="comment__user">{{ c.username }}</span>
							<span class="comment__score"
								>امتیاز: {{ toPersianDigits(c.score) }}/۵</span
							>
						</div>
						<p class="comment__text">{{ c.comment }}</p>
					</li>
				</ul>
				<p v-else class="doctor-details__empty">هنوز نظری ثبت نشده است.</p>
			</section>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.doctor-details {
		padding-left: space(6);
		width: 100%;
		@include flexbox(column, center, center, space(14), nowrap);

		&__state {
			&--loading {
				color: var(--text-500);
			}
			&--error {
				color: var(--danger-500);
			}
		}

		&__container {
			width: 100%;
			@include flexbox(column, center, center, space(14), nowrap);
		}

		&__section-title {
			color: var(--text-900);
			padding-right: space(4);
			border-right: space(4) solid var(--title-100);
		}

		&__comments {
			width: 100%;
		}

		&__empty {
			color: var(--text-500);
		}

		.comments-list {
			list-style: none;
			padding: 0;
			margin: 0;
			@include flexbox(column, stretch, start, space(6), nowrap);
		}

		.comment {
			background-color: var(--bg-400);
			border: space(1) solid var(--text-500);
			border-radius: space(4);
			padding: space(6);
			@include flexbox(column, center, start, space(2), nowrap);
		}

		.comment__meta {
			@include flexbox(row, center, center, space(4), wrap);
		}

		.comment__user {
			color: var(--primary-500);
			font-weight: 600;
		}

		.comment__score {
			color: var(--text-600);
			font-size: 0.875rem;
		}

		.comment__text {
			color: var(--text-900);
			margin: 0;
			line-height: 1.6;
		}
	}
</style>
