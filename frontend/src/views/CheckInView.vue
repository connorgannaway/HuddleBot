<script setup>
import CheckInForm from '../components/CheckInForm.vue'
import axios from 'axios'
import { onMounted, ref } from 'vue';
import {useRoute} from 'vue-router'
import JiraIssue from '../components/JiraIssue.vue'

const validUUID = ref(false)
const retryUUID = ref(false)
const route = useRoute()
const uuid = ref(route.query.uuid)
const inProgressIDs = ref([])
const testingIDs = ref([])
const doneIDs = ref([])
const jiratoken = ref()
const formData = ref()

//check if uuid is a valid uuid from database. Form & issues will only load
//if the uuid is valid
function checkUUID(){
    if(uuid.value){
        axios.get(
            `http://localhost:8000/api/check-in/${uuid.value}/`,
        )
        .then((res) => {
            if(res.status == 200){
                formData.value = res.data
                //console.log(res.data)
                validUUID.value = true
                fetchTicketIDs()
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

function getToken(){
    axios.get(
        'http://localhost:8000/api/token/?service=jira'
    )
    .then((res) => {
        jiratoken.value = res.data.token
    })
    .catch((err) => {
        console.log(err)
    })
}

//handle checkUUID button press
function updateUUID(){
    route.query.uuid = uuid.value
    checkUUID()
    retryUUID.value = true
}

//get uuid's related tickets. sort by status for display
function fetchTicketIDs(){
    axios.get(
        `http://localhost:8000/api/check-in/${uuid.value}/ticketdata/`
    )
    .then((res) => {
        //console.log(res)

        for(const ticket of res.data.in_progress){
            inProgressIDs.value.push({issuekey: ticket})
        }
        for(const ticket of res.data.testing){
            testingIDs.value.push({issuekey: ticket})
        }
        for(const ticket of res.data.done){
            doneIDs.value.push({issuekey: ticket})
        }
    })
    .catch((err) => {
        console.log(err)
    })

}

onMounted(() => {
    getToken()
    checkUUID()
})

</script>

<template>
    <!--IF UUID IS VALID-->
    <div v-if="validUUID">
        <div class="row">
            <div class="column">
                <CheckInForm :inProgress="inProgressIDs" :testing="testingIDs" :done="doneIDs" />
            </div>
            <div class="column">
                <h1>Tickets In Progress</h1>
                <div v-for="ticket in inProgressIDs">
                    <JiraIssue :id="ticket.issuekey" :jiratoken="jiratoken" />
                </div>
        
                <h1>Tickets In Testing</h1>
                <div v-for="ticket in testingIDs">
                    <JiraIssue :id="ticket.issuekey" :jiratoken="jiratoken" />
                </div>
        
                <h1>Recently Completed Tickets</h1>
                <div v-for="ticket in doneIDs">
                    <JiraIssue :id="ticket.issuekey" :jiratoken="jiratoken" />
                </div>
            </div>
        </div>
    </div>
    
    <!--UUID IS NOT VALID-->
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


@media (min-width: 1024px) {
    .row {
        display: flex;
        justify-content: center;
    }

    .column {
        padding: 1em;
        width: 50%;
    }
}


</style>