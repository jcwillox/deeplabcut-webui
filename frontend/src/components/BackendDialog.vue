<script setup lang="ts">
import AlertCard from "@/components/AlertCard.vue";
import { useErrors, useStore } from "@/stores";
import { useFetch } from "@/utils";
import { useVModel } from "@vueuse/core";
import { ref } from "vue";

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const store = useStore();
const errors = useErrors();
const show = useVModel(props, "modelValue", emit);
const showToken = ref(false);
const { isFetching, execute } = useFetch("/");

// automatically show the dialog on network error
errors.$subscribe((_, state) => {
  if (state.error) {
    show.value = true;
  }
});

const reload = () => {
  window.location.reload();
};

const reset = () => {
  store.backend = "http://127.0.0.1:8000";
  store.token = "";
};
</script>

<template>
  <div>
    <v-dialog v-model="show" :persistent="errors.error">
      <v-card class="parent">
        <v-card-title>Backend Configuration</v-card-title>
        <v-card-content>
          <AlertCard
            v-if="errors.error || !errors.updatedAt"
            title="Disconnected!"
            icon="mdi-wifi-strength-alert-outline"
            color="red"
          >
            <template #subtitle>
              {{ errors.error?.status }} {{ errors.error?.message }}
            </template>
          </AlertCard>
          <AlertCard
            v-else
            title="Connected!"
            icon="mdi-check-circle"
            color="success"
          >
            <template #subtitle>
              Updated At: {{ errors.updatedAt?.toLocaleString() }}
            </template>
          </AlertCard>
          <v-text-field
            label="Backend"
            v-model="store.backend"
            placeholder="http://127.0.0.1:8000"
            clearable
            hide-details
          ></v-text-field>
          <v-text-field
            label="Secret Token"
            v-model="store.token"
            :append-icon="showToken ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showToken ? 'text' : 'password'"
            @click:append="showToken = !showToken"
            clearable
            hide-details
          ></v-text-field>
        </v-card-content>
        <v-card-actions class="justify-end">
          <v-btn color="red" @click="reset">Reset</v-btn>
          <v-spacer />
          <v-btn :disabled="isFetching" @click="execute()">
            <v-progress-circular v-if="isFetching" size="22" indeterminate />
            <span v-else>Test Connection</span>
          </v-btn>
          <v-btn color="blue" @click="reload">Reload</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.v-card.parent {
  width: 500px;
}

.v-card.parent > .v-card-content > *:not(:last-child) {
  margin-bottom: 8px;
}

@media screen and (max-width: 500px) {
  .v-card.parent {
    width: 100vw;
  }
}
</style>
