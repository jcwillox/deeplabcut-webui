<script setup lang="ts">
import AlertCard from "@/components/AlertCard.vue";
import { useErrors, useStore } from "@/stores";
import { useFetch } from "@/utils";
import { ref } from "vue";

const store = useStore();
const errors = useErrors();
const dialog = ref(false);
const showToken = ref(false);
const { isFetching, execute } = useFetch("/");

// automatically show the dialog on network error
errors.$subscribe((_, state) => {
  if (state.error) {
    dialog.value = true;
  }
});

const reload = () => {
  window.location.reload();
};

const reset = () => {
  store.backend = "http://127.0.0.1:8000";
  store.token = "";
};

const openDocs = () => {
  window.location.assign(
    import.meta.env.BASE_URL + "docs/guide/select-backend"
  );
};
</script>

<template>
  <div>
    <v-dialog
      v-model="dialog"
      :persistent="errors.error !== undefined"
      width="500px"
      max-width="calc(100% - 8px)"
    >
      <template #activator="props">
        <slot name="activator" v-bind="props" />
      </template>
      <v-card>
        <v-toolbar density="comfortable">
          <v-toolbar-title>Backend Configuration</v-toolbar-title>
          <v-btn @click="openDocs" icon>
            <v-icon>mdi-help-circle</v-icon>
            <v-tooltip activator="parent" location="bottom" text="Help" />
          </v-btn>
          <v-btn
            v-if="!errors.error"
            icon="mdi-close"
            @click="dialog = false"
          />
        </v-toolbar>
        <div class="content overflow-y-auto pa-4">
          <AlertCard
            v-if="errors.error || !errors.updatedAt"
            title="Disconnected!"
            :details="errors.error?.stack"
            icon="mdi-wifi-strength-alert-outline"
            color="red"
          >
            <template #subtitle>
              {{ errors.error?.message }}
              {{ errors.error?.status && `[${errors.error?.status}]` }}
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
            hide-details
            clearable
          ></v-text-field>
        </div>
        <v-divider />
        <v-card-actions class="justify-end">
          <v-btn color="red" @click="reset">Reset</v-btn>
          <v-spacer />
          <v-btn :loading="isFetching" @click="execute()">
            Test Connection
          </v-btn>
          <v-btn color="blue" @click="reload">Reload</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.v-card > .content > *:not(:last-child) {
  margin-bottom: 8px;
}
</style>
