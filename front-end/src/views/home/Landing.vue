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

	const goToDoctorDetails = ({id}) => {
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
			<section>
				<TheTitle label="درباره ما" has-divider/>
				<p class="content__about-us">
					کلینیکس جایی است که سلامت، تخصص و آرامش در کنار هم معنا پیدا می‌کنند.
					ما در کلینیکس با بهره‌گیری از تیمی مجرب از پزشکان و کادر درمانی
					حرفه‌ای، تلاش می‌کنیم تجربه‌ای متفاوت و مطمئن از خدمات درمانی را برای
					مراجعان فراهم کنیم. در کلینیکس، تمرکز ما بر ارائه خدمات دقیق، به روز و
					مبتنی بر استاندارد های علمی است. از مشاوره‌های تخصصی گرفته تا خدمات
					تشخیصی و درمانی، همه چیز با هدف ارتقای کیفیت زندگی شما طراحی شده است.
					فضای مدرن و آرام کلینیک نیز به گونه‌ای آماده شده تا مراجعان در محیطی
					امن و صمیمی خدمات مورد نیاز خود را دریافت کنند.
				</p>
				<p class="content__about-us">
					ما باور داریم که هر مراجعه‌کننده نیازها و شرایط منحصربه‌فردی دارد. به
					همین دلیل، در کلینیکس رویکرد ما شخصی‌سازی خدمات درمانی و همراهی کامل
					در مسیر بهبود است. پاسخگویی دقیق، نوبت‌دهی منظم و احترام به زمان
					بیماران از اصول اصلی کار ماست. کلینیکس فقط یک مرکز درمانی نیست؛ بلکه
					همراهی قابل اعتماد برای حفظ و ارتقای سلامت شماست.
				</p>
			</section>
			<section class="content__doctors-list">
				<TheTitle label="لیست پزشکان برتر کلینیک" has-divider/>
				<h4 class="content__text">
					برای مشاهده جزییات مربوط به پزشک و رزرو نوبت ، روی کارت پزشک مورد نظر کلیک کنید
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
		@include flexbox(column, center, start, space(10));

		.header {
			width: calc(100% - space(12));
			background-color: var(--primary-600);
			padding: space(10) space(6);
			border-radius: space(10);
			text-align: center;
			@include flexbox(column, center, center, space(20));

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
				width: space(80);
				height: space(30);
			}
		}

		.content {
			width: 100%;
			@include flexbox(column, center, right, space(10));

			&__state {
				color: var(--text-500);
			}

			&__about-us {
				color: var(--text-800);
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
				@include flexbox(row, start, center, space(12));
			}
		}
	}
</style>
