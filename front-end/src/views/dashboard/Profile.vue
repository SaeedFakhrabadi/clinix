<script setup>
	import { ref, computed, onMounted } from 'vue';
	import { useRouter } from 'vue-router';
	import { useToast } from 'vue-toastification';
	import { useForm, useField } from 'vee-validate';
	import { storeToRefs } from 'pinia';
	import { profileSchema } from '@/schemas';
	import { editProfile } from '@/services/auth';
	import { doctorDetails } from '@/services/doctors';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import { addCommas } from '@/utils/addCommas';

	const router = useRouter();
	const toast = useToast();

	const loading = ref(true);
	const loadingError = ref(null);

	const currentUserStore = useCurrentUserStore();
	const { currentUser } = storeToRefs(currentUserStore);

	const isPatient = computed(() => currentUser.value.role.value === 'PATIENT');
	const isDoctor = computed(() => currentUser.value.role.value === 'DOCTOR');

	const { handleSubmit } = useForm({
		validationSchema: profileSchema,
		initialValues: {
			name: '',
			email: '',
			phoneNumber: '',
		},
	});

	const { value: name, errorMessage: nameError } = useField('name');
	const { value: role, errorMessage: roleError } = useField('role');
	const { value: email, errorMessage: emailError } = useField('email');
	const { value: phoneNumber, errorMessage: phoneNumberError } =
		useField('phoneNumber');

	const onSubmit = async () => {
		const toastId = toast.info('...در حال ثبت اطلاعات', {
			timeout: false,
			closeOnClick: false,
		});

		try {
			const response = await editProfile(
				name.value,
				email.value,
				phoneNumber.value,
			);

			const userInfo = response?.data;
			currentUserStore?.setCurrentUser(userInfo);

			toast.dismiss(toastId);
			toast.success(response?.data?.message);
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

			toast.dismiss(toastId);
			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');
		}
	};

	const submitForm = handleSubmit(onSubmit);

	const setDefaultInfo = () => {
		name.value = currentUser.value?.name;
		role.value = currentUser.value.role?.label;
		email.value = currentUser.value?.email;
		phoneNumber.value = currentUser.value?.phoneNumber;
	};

	onMounted(async () => {
		if (isPatient.value) setDefaultInfo();
		if (isDoctor.value) {
			loading.value = true;
			try {
				// const { data } = await doctorDetails(currentUser.value?.did);

				loading.value = false;
			} catch (error) {
				console.error('Error : ', error?.response?.data || error?.message);

				toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');

				loading.value = false;
				loadingError.value = true;
			}
		}
	});
</script>

<template>
	<div class="profile">
		<!-- <div v-if="loading" class="reservations__state--loading">
			<h2>در حال دریافت اطلاعات نوبت ها...</h2>
		</div>
		<div v-else-if="loadingError" class="reservations__state--error">
			<h2>خطا در دریافت اطلاعات نوبت ها!</h2>
		</div> -->
		<h2 class="profile__title">اطلاعات شخصی</h2>
		<form v-if="isPatient" class="profile__form" @submit.prevent="submitForm">
			<div class="profile__sections-patient">
				<section class="profile__section-patient">
					<TheInput
						v-model="name"
						label="نام"
						icon-name="user"
						:error-message="nameError"
					/>
					<TheInput
						v-model="role"
						label="نقش"
						icon-name="user-role"
						is-disabled
					/>
				</section>
				<section class="profile__section-patient">
					<TheInput
						v-model="email"
						label="ایمیل"
						type="email"
						icon-name="email"
						:error-message="emailError"
					/>
					<TheInput
						v-model="phoneNumber"
						label="شماره تماس"
						icon-name="phone"
						digits-only
						:error-message="phoneNumberError"
					/>
				</section>
			</div>
			<section class="profile__section-buttons">
				<TheButton
					type="cancel"
					label="لغو تغییرات"
					@click.prevent="setDefaultInfo"
				/>
				<TheButton type="submit" label="ثبت اطلاعات شخصی" />
			</section>
		</form>
		<div v-if="isDoctor" class="profile__container">
			<div class="profile__sections-doctor">
				<section class="profile__section-doctor">
					<div class="profile__item item">
						<span class="item__label">نام:</span>
						<h3 class="item__value">دکتر {{ currentUser.name }}</h3>
					</div>
					<div class="profile__item item">
						<span class="item__label">شماره تلفن:</span>
						<h3 class="item__value">
							{{ toPersianDigits(currentUser.phoneNumber) }}
						</h3>
					</div>
				</section>
				<section class="profile__section-doctor">
					<div class="profile__item item">
						<span class="item__label">ایمیل:</span>
						<h3 class="item__value">{{ currentUser.email }}</h3>
					</div>
				</section>
			</div>
		</div>
		<h2 v-if="isDoctor" class="profile__title">اطلاعات پزشکی</h2>
		<div v-if="isDoctor" class="profile__container">
			<div class="profile__sections-doctor">
				<section class="profile__section-doctor">
					<div class="profile__item item">
						<span class="item__label">تخصص:</span>
						<h3 class="item__value">{{ currentUser.name }}</h3>
					</div>
					<div class="profile__item item">
						<span class="item__label">سابقه کار:</span>
						<h3 class="item__value">{{ toPersianDigits(12) }} سال</h3>
					</div>
				</section>
				<section class="profile__section-doctor">
					<div class="profile__item item">
						<span class="item__label">قیمت ویزیت (ساعت):</span>
						<h3 class="item__value">{{ addCommas(200000) }}</h3>
					</div>
					<div class="profile__item item">
						<span class="item__label">میانگین امتیازات دریافتی:</span>
						<h3 class="item__value">{{ toPersianDigits(`4.7 از 5`) }}</h3>
					</div>
				</section>
				<section class="profile__section-doctor">
					<div class="profile__item item">
						<span class="item__label">موقعیت مطب:</span>
						<h3 class="item__value">{{ currentUser.name }}</h3>
					</div>
				</section>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.profile {
		// &__state {
		// 	&--loading {
		// 		color: var(--text-500);
		// 	}
		// 	&--error {
		// 		color: var(--danger-500);
		// 	}
		// }

		&__title {
			color: var(--text-900);
			padding-right: space(4);
			border-right: space(4) solid var(--title-100);
		}

		&__form {
			width: 100%;
			@include flexbox(column, center, center, space(10));
		}

		&__sections-patient {
			width: 100%;
			@include flexbox(column, center, center, space(0));
		}

		&__section-patient {
			width: 100%;
			@include flexbox(row, center, start, space(10), nowrap);

			@media (max-width: $md) {
				@include flexbox(column, center, start, space(0));
			}
		}

		&__section-buttons {
			width: 100%;
			@include flexbox(row, center, start, space(10), nowrap);

			@media (max-width: $md) {
				@include flexbox(column, center, start, space(14));
			}
		}

		&__container {
			width: 100%;
			padding-block: space(10);
			@include flexbox(column, center, start, space(10));
		}

		&__sections-doctor {
			width: 100%;
			@include flexbox(column, center, center, space(10));

			@media (max-width: $lg) {
				@include flexbox(column, center, start, space(0));
			}
		}

		&__section-doctor {
			width: 100%;
			@include flexbox(row, center, start, space(0), nowrap);

			@media (max-width: $lg) {
				@include flexbox(column, center, start, space(0));
			}
		}

		.item {
			width: 100%;
			@include flexbox(row, start, center, space(2), nowrap);

			&__label {
				font-size: space(10);
				color: var(--text-400);
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
</style>
