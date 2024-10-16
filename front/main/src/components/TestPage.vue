<template>
  <div class="dashboard-container">
    <h2>Tableau de bord</h2>
    <div class="card">
      <DataTable :value="profiles" editMode="row" dataKey="id" @row-edit-save="onRowEditSave"
        :pt="{
            table: { style: 'min-width: 50rem' },
            column: {
                bodycell: ({ state }) => ({
                    style:  state['d_editing'] && 'padding-top: 0.75rem; padding-bottom: 0.75rem'
                })
            }
        }"
      >
        <Column field="id" header="ID" style="width: 10%">
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" fluid />
          </template>
          <template #body="{ data, field }">
            {{ data[field] }}
          </template>
        </Column>
        <Column field="account" header="Account" style="width: 20%">
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" fluid />
          </template>
          <template #body="{ data, field }">
            {{ data[field] }}
          </template>
        </Column>
        <Column field="content" header="Content" style="width: 30%">
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" fluid />
          </template>
          <template #body="{ data, field }">
            {{ data[field] }}
          </template>
        </Column>
        <Column field="social" header="Social" style="width: 20%">
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" fluid />
          </template>
          <template #body="{ data, field }">
            {{ data[field] }}
          </template>
        </Column>
        <Column field="score" header="Score" style="width: 20%">
          <template #editor="{ data, field }">
            <InputNumber v-model="data[field]" mode="decimal" :min="0" :max="5" :step="0.1" fluid />
          </template>
          <template #body="{ data, field }">
            <div :class="['score-box', { 'score-meow': data[field] === 'non-suicide', 'score-other': data[field] !== 'non-suicide' }]">
              {{ data[field] }}
            </div>
          </template>
        </Column>
        <Column :rowEditor="true" style="width: 10%; min-width: 8rem" bodyStyle="text-align:center"></Column>
      </DataTable>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';

export default {
  name: 'DashboardPage',
  components: {
    DataTable,
    Column,
    InputText,
    InputNumber
  },
  setup() {
    const profiles = ref([]);
    const editingRows = ref([]);

    const fetchProfiles = () => {
      axios.get('http://127.0.0.1:8000/get-processed-messages')
        .then(response => {
          if (Array.isArray(response.data.processed_messages)) {
            profiles.value = response.data.processed_messages ? [...response.data.processed_messages] : [];
            console.log(response.data.processed_messages);
          } else {
            console.error('Полученные данные не являются массивом:', response.data);
          }
        })
        .catch(error => {
          console.error('Erreur lors de la récupération des données:', error);
        });
    };

    const onRowEditSave = (event) => {
      let { newData, index } = event;
      profiles.value[index] = newData;
    };

    fetchProfiles();

    return {
      profiles,
      editingRows,
      onRowEditSave
    };
  }
};
</script>

<style scoped>
.dashboard-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}
.card {
  margin-top: 40px;
}
.score-box {
  padding: 10px;
  margin: 5px;
  display: inline-block;
  border-radius: 5px;
  font-weight: bold;
}

.score-meow {
  color: green;
  background-color: lightgreen;
}

.score-other {
  color: red;
  background-color: lightcoral;
}
</style>