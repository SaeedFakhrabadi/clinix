<script setup>
	import { ref, onMounted, onUnmounted } from 'vue';

	const props = defineProps({
		initialMinutes: {
			type: Number,
			default: 2,
		},
	});

	const timer = ref('02:00');
	let timerInterval = null;

	const startTimer = () => {
		let totalSeconds = props.initialMinutes * 60;

		timerInterval = setInterval(() => {
			totalSeconds--;

			if (totalSeconds < 0) {
				clearInterval(timerInterval);
				timer.value = '00:00';
				return;
			}

			const minutes = Math.floor(totalSeconds / 60);
			const seconds = totalSeconds % 60;
			timer.value = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
		}, 1000);
	};

	onMounted(() => {
		startTimer();
	});

	onUnmounted(() => {
		clearInterval(timerInterval);
	});
</script>

<template>
	<h5 class="countdown-timer">{{ timer }}</h5>
</template>

<style lang="scss" scoped>
	.countdown-timer {
		user-select: none;
		position: absolute;
		color: var(--danger-100);
	}
</style>
