<script setup>
    import {ref} from 'vue'
    import axios from 'axios'

    const first_name = ref()
    const last_name = ref()
    const slack_id = ref()
    const jira_id = ref()
    const start_date = ref()
    const end_date = ref()
    const is_active = ref(true)
    let slack_token = ''
    const matchFound = ref(false)
    const attemptMatch = ref(false)

    
    async function getSlackToken(){
        axios.get(
            'http://localhost:8000/api/token/?type=slack'
        ).then((res) => {
            slack_token = res.data.token
        })
        .catch((err) => {
            console.log(err)
        })
    }

    function postTest(e){
        e.preventDefault()

        const body = `token=${slack_token}`

        axios.post('https://slack.com/api/users.list', body)
        .then((res) => {
            let members = res.data.members
            for(const member of members){
                if(member.real_name == `${first_name.value} ${last_name.value}`){
                    slack_id.value = member.id
                    matchFound.value = true
                }
                
            }
            attemptMatch.value = true

        })
        .catch((err) => {
            console.log(err)
        })
    }
    
    
    (() => {
        getSlackToken()
    })()

</script>



<template>

    <form>
        <h1>Create Person</h1>
        <label>First Name</label>
        <input v-model="first_name" />

        <label>Last Name</label>
        <input v-model="last_name" />
        <label>Slack ID - 
            <button @click="postTest">Search</button> 
            <p v-if="matchFound && attemptMatch" class="success">Match Found</p> 
            <p v-if="attemptMatch && !matchFound" class="error">No Match Found</p>
        </label>
        <input v-model="slack_id" />

        <label>Jira ID</label>
        <input v-model="jira_id" />

        <label>Start Date</label>
        <input type="date" v-model="start_date" />

        <label>End Date</label>
        <input type="date" v-model="end_date" />

        <label>Active</label>
        <input type="checkbox" v-model="is_active" />
    </form>

</template>

<style scoped>
    h1 {
        font-weight: 400;
    }
    form {
        text-align: left;
        padding: 30px;
        border-radius: 10px;
        background: white;
        max-width: 400px;
        min-width: 25vw;
    }
    label {
        display: inline-block;
        margin: 10px 0 5px;
        font-size: 1rem;
        text-transform: uppercase;
        font-weight: normal;

    }
    input {
        display: block;
        padding: 10px 6px;
        width: 100%;
        box-sizing: border-box;
        border: none;
        border-bottom: 2px solid #ddd;
    }
    .success {
        color:green;
    }
    .error {
        color: red;
    }
</style>
