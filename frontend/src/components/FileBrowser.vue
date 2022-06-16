<script setup lang="ts">
import { humanizeBytes } from "@/utils";
import { useVModel } from "@vueuse/core";
import { capitalize } from "vue";

export interface ItemBase {
  name: string;
  [key: string]: unknown;
}

/* eslint-disable @typescript-eslint/no-explicit-any */
export interface Column<T extends ItemBase = ItemBase> {
  name?: string;
  field?: string;
  type?: "icon" | "unix" | "bytes";
  default?: any;
  getter?: (value: any, item: T, column: Column<T>) => unknown;
  align?: "left" | "center" | "right";
  shrink?: boolean;
}

const props = defineProps<{
  items?: ItemBase[] | null;
  loading?: boolean;
  selected: string;
  height?: string;
  columns: Column[];
}>();

const emit = defineEmits<{
  (e: "update:selected", selected: string): void;
}>();

const selected = useVModel(props, "selected", emit);
const locale = navigator.language !== "en-US" ? navigator.language : undefined;
const formatDate = Intl.DateTimeFormat(locale, {
  day: "2-digit",
  month: "2-digit",
  year: "numeric",
  hour: "numeric",
  minute: "2-digit"
});

const resolveColumn = (column: Column, item: ItemBase) => {
  let value = column.field ? item[column.field] : undefined;
  value = column.getter ? column.getter(value, item, column) : value;
  if (value) {
    switch (column.type) {
      case "unix":
        return formatDate
          .format(new Date((value as number) * 1000))
          .toUpperCase();
      case "bytes":
        return humanizeBytes(value as number);
      default:
        return value;
    }
  }
  return column.default;
};
</script>

<template>
  <v-table :height="height" class="position-relative" fixed-header>
    <thead>
      <tr>
        <th
          v-for="(column, i) in columns"
          :key="i"
          :class="{
            icon: column.type === 'icon',
            center: column.align === 'center',
            right: column.align === 'right',
            shrink: column.shrink
          }"
        >
          {{ column.name || (column.field && capitalize(column.field)) }}
        </th>
      </tr>
    </thead>
    <v-progress-linear
      v-if="loading"
      class="position-absolute"
      color="primary"
      indeterminate
    />
    <tbody v-if="!loading || items">
      <tr
        v-for="(item, i) in items"
        :key="i"
        :class="{ active: selected === item.name }"
        @click="selected = item.name"
      >
        <td
          v-for="(column, i) in columns"
          :key="i"
          :class="{
            icon: column.type === 'icon',
            center: column.align === 'center',
            right: column.align === 'right',
            shrink: column.shrink
          }"
        >
          <v-icon v-if="column.type === 'icon'">
            {{ resolveColumn(column, item) }}
          </v-icon>
          <span v-else>
            {{ resolveColumn(column, item) }}
          </span>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<style scoped>
tr {
  cursor: pointer;
}
tr.active {
  background: rgba(var(--v-border-color), var(--v-selected-opacity));
}

td.icon,
th.icon {
  width: 0.1%;
  padding-right: 4px !important;
  white-space: nowrap;
  text-align: center;
}
td.center,
th.center {
  text-align: center;
}
td.right,
th.right {
  text-align: right;
}
td.shrink,
th.shrink {
  width: 0.1%;
  white-space: nowrap;
}
</style>
