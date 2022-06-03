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
  window.location.assign(import.meta.env.BASE_URL + "docs/");
};
</script>

<template>
  <div>
    <v-dialog
      v-model="dialog"
      v-bind="{ persistent: errors.error !== undefined }"
    >
      <template #activator="props">
        <slot name="activator" v-bind="props" />
      </template>
      <v-card class="parent">
        <v-toolbar class="toolbar-fixed">
          <v-toolbar-title>Backend Configuration</v-toolbar-title>
          <v-btn @click="openDocs" icon>
            <v-icon class="text-high-emphasis">mdi-help-circle</v-icon>
            <v-tooltip
              v-bind="{ activator: 'parent' }"
              location="bottom"
              text="Help"
            />
          </v-btn>
          <v-btn
            v-if="!errors.error"
            icon="mdi-close"
            @click="dialog = false"
          />
        </v-toolbar>
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
            hide-details
            clearable
          ></v-text-field>
        </v-card-content>
        <v-divider />
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
