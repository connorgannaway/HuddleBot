<script setup>
import CheckInForm from '../components/CheckInForm.vue'
import axios from 'axios'
import { onMounted, ref } from 'vue';
import {useRoute} from 'vue-router'

const validUUID = ref(false)
const retryUUID = ref(false)
const route = useRoute()
const uuid = ref(route.query.uuid)

function checkUUID(){
    if(uuid.value){
        axios.get(
            'http://localhost:8000/api/check-in/' + uuid.value,
        )
        .then((res) => {
            if(res.status == 200){
                validUUID.value = true
            }
        })
        .catch((err) => {
            console.log(err)
            validUUID.value = false
        })
    }
    else{
        validUUID.value = false
    }
}

function updateUUID(){
    route.query.uuid = uuid.value
    checkUUID()
    retryUUID.value = true
}

onMounted(() => {
    checkUUID()
})

</script>

<template>
    <div v-if="validUUID">
        <CheckInForm />
    </div>
    <div v-else>
        <h1>UUID Needed</h1>
        <p>UUID either not provided or not found in the database.</p>
        <hr />
        <div>
            <input v-model="uuid" type="text" />
            <button @click="updateUUID">Check UUID</button>
        </div>
        <p v-if="retryUUID && validUUID == false" class="error">Invalid UUID</p>
        
    </div>
</template>

<style scoped>

hr {
    margin: 10px 0 10px;
}
.error {
    color: red;
}
button {
    margin-left: 10px;
}


</style>