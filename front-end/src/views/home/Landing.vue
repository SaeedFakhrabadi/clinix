<script setup>
	import { computed, onMounted, ref } from 'vue';
	import { useRouter } from 'vue-router';
	import { useToast } from 'vue-toastification';
	import { doctorsList } from '@/services/doctors';

	const router = useRouter();
	const toast = useToast();

	const doctors = ref([]);

	const loading = ref(false);

	const mappedDoctors = computed(() => {
		return doctors.value.filter((doctor) => doctor.score >= 4);
	});

	const goToDoctorDetails = ({ id }) => {
		router.push({
			name: 'DoctorDetails',
			query: { did: id },
		});
	};

	onMounted(async () => {
		loading.value = true;
		try {
			const response = await doctorsList();
			doctors.value = response.data;
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');

			doctors.value = [];
		} finally {
			loading.value = false;
		}
	});
</script>

<template>
	<div class="landing">
		<header class="landing__header header">
			<img src="/landing.png" class="header__image" />
			<h1 class="header__slogan">
				کلینیکس، بزرگترین کلینیک آنلاین مدیریت و رزرو نوبت های پزشکی
			</h1>
			<h3 class="header__sub-slogan">
				همین الآن برای مشاهده لیست پزشکان و رزرو نوبت کلیک کنید
			</h3>
			<TheButton
				class="header__button"
				type="submit"
				label="مشاهده لیست پزشکان"
				@click="() => router.push({ name: 'DoctorsList' })"
			/>
		</header>
		<main class="home__content content">
			<AboutUs />
			<section class="content__doctors-list">
				<TheTitle label="لیست پزشکان برتر کلینیک" has-divider />
				<h4 class="content__text">
					برای مشاهده جزییات مربوط به پزشک و رزرو نوبت ، روی کارت پزشک مورد نظر
					کلیک کنید
				</h4>
				<div v-if="loading" class="content__state">
					<h2>در حال دریافت اطلاعات پزشکان...</h2>
				</div>
				<ul v-else class="content__list">
					<DoctorCard
						v-for="doctor in mappedDoctors"
						:id="doctor?.id"
						:name="doctor?.name"
						:field="doctor?.field"
						:location="doctor?.location"
						:price="doctor?.price"
						:score="doctor?.score"
						@select="goToDoctorDetails"
					/>
				</ul>
			</section>
		</main>
	</div>
</template>

<style lang="scss" scoped>
	.landing {
		.header {
			width: 100%;
			padding: space(10) space(6);
			border-radius: space(10);
			box-sizing: border-box;
			text-align: center;
			position: relative;
			background-image: linear-gradient(
				0deg,
				var(--primary-100),
				rgba(0, 0, 0, 0)
			);
			z-index: 1;
			@include flexbox(column, center, center, space(20));

			&__image {
				width: 100%;
				height: 100%;
				border-radius: space(10);
				object-fit: cover;
				opacity: 0.3;
				position: absolute;
				z-index: -1;
			}

			&__slogan {
				color: var(--title-600);
				animation: subtle-shake 3s infinite alternate ease;
				@include flexbox(row, center, center, space(0), wrap);
			}

			@keyframes subtle-shake {
				0% {
					transform: translate(space(0), space(0));
				}
				25% {
					transform: translate(space(0), space(2));
				}
				50% {
					transform: translate(space(0), space(0));
				}
				75% {
					transform: translate(space(0), space(2));
				}
			}

			&__sub-slogan {
				color: var(--title-400);
			}

			&__button {
				width: space(100);
				height: space(30);
				background-color: var(--title-500);
				color: var(--bg-900);

				&:hover {
					background-color: var(--title-300);
				}
			}
		}

		.content {
			width: 100%;
			@include flexbox(column, center, right, space(10));

			&__state {
				color: var(--text-500);
			}

			&__doctors-list {
				@include flexbox(column, start, start, space(10), nowrap);
			}

			&__text {
				color: var(--text-900);
			}

			&__list {
				width: 100%;
				user-select: none;
				@include flexbox(row, start, center, space(8));
			}
		}
	}
</style>
