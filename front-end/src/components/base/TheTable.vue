<script setup>
	import { toPersianDigits } from '@/utils/toPersianDigits';

	const props = defineProps({
		headers: { type: Array, required: true },
		rows: { type: Array, required: true },
		loading: { type: Boolean, default: false },
		clickMode: {
			type: String,
			default: 'row',
			validator: (v) => ['cell', 'row', 'readOnly'].includes(v),
		},
		getCellClass: { type: Function, default: undefined },
	});

	const emit = defineEmits(['row-click', 'cell-click']);

	const isClickable = (mode) => mode !== 'readOnly';
	const isRowMode = (mode) => mode === 'row';
	const isCellMode = (mode) => mode === 'cell';

	const handleRowClick = (row, index) => {
		if (props.clickMode !== 'row') return;
		emit('row-click', { row, index });
	};

	const handleCellClick = (row, header) => {
		const firstHeader = props.headers[0];
		const firstCellValue = row[firstHeader.value];
		const cellValue = row[header.value];
		emit('cell-click', {
			header: { label: header.label, value: header.value },
			firstCellValue,
			cellValue,
		});
	};

	const onCellClick = (e, row, header) => {
		if (props.clickMode === 'cell') {
			e.stopPropagation();
			handleCellClick(row, header);
		}
	};
</script>

<template>
	<div class="the-table">
		<div v-if="loading" class="the-table__state">
			<h2>در حال دریافت اطلاعات...</h2>
		</div>
		<div v-else-if="!rows?.length" class="the-table__state">
			<h2>اطلاعاتی برای نمایش پیدا نشد!</h2>
		</div>
		<table
			v-else
			class="the-table__table table"
			:class="{
				'table--row-click': isRowMode(clickMode),
				'table--cell-click': isCellMode(clickMode),
				'table--read-only': clickMode === 'readOnly',
			}"
		>
			<thead class="table__head">
				<tr>
					<th v-if="isRowMode(clickMode)" class="table__head-cell">
						ردیف
					</th>
					<th
						v-for="header in headers"
						:key="header.value"
						class="table__head-cell"
					>
						<h4>{{ toPersianDigits(header.label) }}</h4>
					</th>
				</tr>
			</thead>
			<tbody class="table__body">
				<tr
					v-for="(row, index) in rows"
					:key="index"
					class="table__row"
					:class="{ 'table__row--clickable': isClickable(clickMode) }"
					@click="handleRowClick(row, index)"
				>
					<td v-if="isRowMode(clickMode)" class="table__body-cell">
						{{ toPersianDigits(index + 1) }}
					</td>
					<td
						v-for="header in headers"
						:key="header.value"
						class="table__body-cell"
						:class="[
							{
								'table__body-cell--clickable': isCellMode(clickMode),
							},
							getCellClass ? getCellClass(row[header.value]) : '',
						]"
						@click="onCellClick($event, row, header)"
					>
						<h4>{{ toPersianDigits(row[header.value]) }}</h4>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<style lang="scss" scoped>
	.the-table {
		width: 100%;
		@include flexbox();

		&__state {
			color: var(--text-500);
		}

		.table {
			width: 100%;
			border-collapse: collapse;

			&__head {
				background-color: var(--primary-300);
			}

			&__head-cell {
				color: var(--text-900);
				padding-block: space(6);
				border-inline: space(0.5) solid var(--bg-900);

				&:first-child {
					border-right: none;
					border-top-right-radius: space(6);
				}
				
				&:last-child {
					border-left: none;
					border-top-left-radius: space(6);
				}
			}

			&__head-cell h4 {
				@media (max-width: $md) {
					font-size: $font-size-md;
				}
				@media (max-width: $sm) {
					font-size: $font-size-sm;
				}
			}

			&__body-cell {
				color: var(--text-900);
				padding-block: space(4);
				border: space(0.5) solid var(--primary-300);
				text-align: center;

				&--clickable {
					cursor: pointer;
				}
			}

			&__body-cell h4 {
				@media (max-width: $md) {
					font-size: $font-size-md;
				}
				@media (max-width: $sm) {
					font-size: $font-size-sm;
				}
			}

			&__row {
				&:nth-child(odd) {
					background-color: var(--bg-900);
				}

				&:nth-child(even) {
					background-color: var(--bg-700);
				}

				& td:first-child {
					border-right: none;
				}

				& td:last-child {
					border-left: none;
				}

				&:last-child td{
					border-bottom: none;
				}

				&:last-child td:first-child {
					border-bottom-right-radius: space(6);
				}

				&:last-child td:last-child {
					border-bottom-left-radius: space(6);
				}
			}

			&--row-click .table__row--clickable {
				cursor: pointer;
			}

			&--row-click .table__row--clickable:hover {
				background-color: var(--primary-600);
			}

			&--cell-click .table__body-cell--clickable:hover {
				background-color: var(--primary-600);
			}

			&--cell-click .table__body-cell--clickable:first-child {
					cursor: auto;
					background-color: inherit;
			}

			&--read-only .table__row,
			&--read-only .table__body-cell {
				cursor: default;
			}
		}
	}
</style>
