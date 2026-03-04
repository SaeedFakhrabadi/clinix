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
	import { addCommas } from '@/utils/addCommas';
	import { toPersianDigits } from '@/utils/toPersianDigits';
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

		const isCommented = doctor.value?.comments.find((c)=> c?.username === currentUser.value?.name);
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
			<section class="doctor-details__info info">
				<h2 class="doctor-details__section-title">اطلاعات پزشک</h2>
				<div class="info__sections-doctor">
					<h2 class="info__name">دکتر {{ doctor?.name }}</h2>
					<section class="info__section-doctor">
						<div class="info__item item">
							<span class="item__label">تخصص:</span>
							<h3 class="item__value">{{ doctor?.field }}</h3>
						</div>
						<div class="info__item item">
							<span class="item__label">سابقه کار:</span>
							<h3 class="item__value">
								{{ toPersianDigits(doctor?.experience || 0) }} سال
							</h3>
						</div>
					</section>
					<section class="info__section-doctor">
						<div class="info__item item">
							<span class="item__label">قیمت ویزیت (ساعت):</span>
							<h3 class="item__value">{{ addCommas(doctor?.price) }}</h3>
						</div>
						<div class="info__item item">
							<span class="item__label">میانگین امتیازات دریافتی:</span>
							<h3 v-if="doctor?.score !== 0" class="item__value">
								{{ toPersianDigits(`${doctor?.score} از 5`) }}
							</h3>
							<h3 v-else class="item__value">بدون امتیاز</h3>
						</div>
					</section>
					<section class="info__section-doctor">
						<div class="info__item item">
							<span class="item__label">موقعیت مطب:</span>
							<h3 class="item__value">{{ doctor?.location }}</h3>
						</div>
						<div class="info__item item">
							<span class="item__label">ساعت کاری:</span>
							<h3 class="item__value">
								از {{ toPersianDigits(doctor?.start_working_hour) }} تا
								{{ toPersianDigits(doctor?.end_working_hour) }}
							</h3>
						</div>
					</section>
				</div>
			</section>
			<ScheduleTable :doctor="doctor" :currentUser="currentUser" @pay="pay" />
			<section class="doctor-details__comments comments">
				<h2 class="doctor-details__section-title">نظرات کاربران</h2>
				<h2 v-if="!doctor?.comments?.length" class="comments__empty">
					هنوز نظری ثبت نشده است!
				</h2>
				<Comments v-else :comments="doctor?.comments"/>
				<h2 class="doctor-details__section-title">ثبت نظر و امتیاز دهی</h2>
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

		.info {
			width: 100%;
			@include flexbox(column, center, start, space(10), nowrap);

			&__sections-doctor {
				width: calc(100% - space(12));
				background-color: var(--primary-500);
				padding: space(6);
				border-radius: space(10);
				@include flexbox(column, center, center, space(4));

				@media (max-width: $md) {
					@include flexbox(column, center, start, space(0));
				}
			}

			&__name {
				width: 100%;
				text-align: center;
				border-bottom: space(0.5) solid var(--text-500);
				color: var(--title-500);
				padding-bottom: space(6);
				margin-bottom: space(6);
			}

			&__section-doctor {
				width: 100%;
				@include flexbox(row, center, start, space(0), nowrap);

				@media (max-width: $md) {
					@include flexbox(column, center, start, space(0));
				}
			}

			.item {
				width: 100%;
				@include flexbox(row, start, center, space(2), nowrap);

				&__label {
					font-size: space(10);
					color: var(--text-600);
					@include lineClamp(1);

					@media (max-width: $md) {
						font-size: space(8);
					}
				}

				&__value {
					color: var(--text-800);
					@include lineClamp(1);

					@media (max-width: $md) {
						font-size: space(8);
					}
				}
			}
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

				@media (min-width: $xl) {
					width: calc(100% - space(0.5));
					margin-right: space(0.5);
				}
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
