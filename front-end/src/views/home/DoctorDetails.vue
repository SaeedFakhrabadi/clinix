<script setup>
	import { computed, onMounted, ref } from 'vue';
	import { useRoute, useRouter } from 'vue-router';
	import { useForm, useField } from 'vee-validate';
	import { useToast } from 'vue-toastification';
	import { storeToRefs } from 'pinia';
	import { commentSchema } from '@/schemas';
	import { doctorDetails, createComment } from '@/services/doctors';
	import { createReservation } from '@/services/reservations';
	import { createTransaction } from '@/services/transactions';
	import { useCurrentUserStore } from '@/stores/currentUser';

	const route = useRoute();
	const router = useRouter();
	const toast = useToast();

	const currentUserStore = useCurrentUserStore();
	const { currentUser } = storeToRefs(currentUserStore);

	const doctor = ref(null);

	const loading = ref(true);
	const loadingError = ref(false);

	const did = computed(() => route.query.did);

	const { handleSubmit } = useForm({
		validationSchema: commentSchema,
		initialValues: {
			comment: '',
			score: 5,
		},
	});

	const { value: comment, errorMessage: commentError } = useField('comment');
	const { value: score, errorMessage: scoreError } = useField('score');

	const onSubmit = async () => {
		if (!currentUser.value) {
			router.push({ name: 'Login' });
			toast.error('!برای ثبت نظر و امتیاز دهی ابتدا وارد حساب کاربری خود شوید');
			return;
		}

		if (currentUser.value?.role?.value === 'DOCTOR') {
			toast.error('!امکان ثبت نظر و امتیاز دهی برای پزشکان وجود ندارد');
			return;
		}

		const isCommented = doctor.value?.comments.find(
			(c) => c?.username === currentUser.value?.name,
		);
		if (isCommented) {
			toast.error('!شما قبلا نظر خود را برای این پزشک ثبت کرده اید');
			return;
		}

		const toastId = toast.info('...در حال ثبت اطلاعات', {
			timeout: false,
			closeOnClick: false,
		});

		try {
			await createComment(
				currentUser.value?.id,
				doctor.value?.did,
				comment.value,
				score.value,
			);

			toast.dismiss(toastId);

			location.reload();
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.dismiss(toastId);
			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');
		}
	};
	const submitForm = handleSubmit(onSubmit);

	const pay = async (data) => {
		const toastId = toast.info('...در حال ثبت اطلاعات', {
			timeout: false,
			closeOnClick: false,
		});

		try {
			await createReservation(
				data?.reservationData.value?.did,
				data?.reservationData.value?.pid,
				data?.reservationData.value?.time,
			);

			await createTransaction(
				data?.transactionData.value?.method,
				data?.transactionData.value?.pid,
				data?.transactionData.value?.price,
				data?.transactionData.value?.type,
			);

			toast.dismiss(toastId);
			toast.success('پرداخت با موفقیت انجام و نوبت رزرو شد');

			router.push({ name: 'Reservations' });
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.dismiss(toastId);
			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');
		}
	};

	onMounted(async () => {
		loading.value = true;
		try {
			const response = await doctorDetails(did.value);
			doctor.value = response?.data;

			loading.value = false;
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');

			loading.value = false;
			loadingError.value = true;
		}
	});
</script>

<template>
	<div class="doctor-details">
		<div v-if="loading" class="doctor-details__state--loading">
			<h2>در حال دریافت اطلاعات پزشک...</h2>
		</div>
		<div v-else-if="loadingError" class="doctor-details__state--error">
			<h2>خطا در دریافت اطلاعات پزشک!</h2>
		</div>
		<div v-else class="doctor-details__container">
			<DoctorInfo :doctor="doctor"/>

			<ScheduleTable :doctor="doctor" :currentUser="currentUser" @pay="pay" />
			
			<section class="doctor-details__comments comments">
				<TheTitle label="نظرات کاربران" has-divider />
				<h2 v-if="!doctor?.comments?.length" class="comments__empty">
					هنوز نظری ثبت نشده است!
				</h2>
				<Comments v-else :comments="doctor?.comments" />
				<TheTitle label="ثبت نظر و امتیاز دهی" has-divider />
				<form class="comments__form" @submit.prevent="submitForm">
					<TheInput
						type="textarea"
						icon-name="message-check"
						v-model="comment"
						:error-message="commentError"
						label="ثبت نظر"
						placeholder="لطفا نظر خود را درباره این پزشک ثبت کنید..."
					/>
					<div class="comments__row">
						<TheSelect
							v-model="score"
							label="امتیاز"
							icon-name="star"
							:options="[
								{ label: '5 ستاره', value: '5' },
								{ label: '4 ستاره', value: '4' },
								{ label: '3 ستاره', value: '3' },
								{ label: '2 ستاره', value: '2' },
								{ label: '1 ستاره', value: '1' },
							]"
						/>
						<TheButton
							type="submit"
							label="ثبت نظر و امتیاز"
							class="comments__button"
						/>
					</div>
				</form>
			</section>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.doctor-details {
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

		.comments {
			width: 100%;
			@include flexbox(column, center, start, space(10), nowrap);

			&__empty {
				color: var(--text-500);
			}

			&__form {
				width: 100%;
				@include flexbox(column, center, start, space(0), nowrap);
			}

			&__row {
				width: 100%;
				@include flexbox(row, center, end, space(10), nowrap);

				@media (max-width: $sm) {
					@include flexbox(column, center, end, space(10), nowrap);
				}
			}

			&__button {
				margin-bottom: space(4);
			}
		}
	}
</style>
