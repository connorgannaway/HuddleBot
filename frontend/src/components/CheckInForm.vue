<script setup>
    import {onMounted, ref} from 'vue'
    import axios from 'axios'
    import { useRoute } from 'vue-router';

    const feeling = ref()
    const prior_work = ref()
    const planned_work = ref()
    const blockers = ref()

    let slack_token = ''
    let jira_token = ''

    const route = useRoute()
    const postCode = ref()

    
    
    function getTokens(){
        axios.get(
            'http://localhost:8000/api/token/?service=slack'
        )
        .then((res) => {
            slack_token = res.data.token
        })
        .catch((err) => {
            console.log(err)
        })

        axios.get(
            'http://localhost:8000/api/token/?service=jira'
        )
        .then((res) => {
            jira_token = res.data.token
        })
        .catch((err) => {
            console.log(err)
        })
    }

    

    function sumbitForm(e){
        e.preventDefault()
        
        let params = {
            feeling: feeling.value,
            prior_work: prior_work.value,
            planned_work: planned_work.value,
            blockers: blockers.value,
        }
    

        axios.patch(
            'http://localhost:8000/api/check-in/' + route.query.uuid + '/',
            params
        )
        .then((res) => {
            console.log(res)
            postCode.value = res.status
        })
        .catch((err) => {
            console.log(err)
            postCode.value = err.response.status
        })
    }
    
    
    onMounted(() => {
        //getTokens()
    })

</script>



<template>

    <form>
        <h1>Daily Check-In</h1>
        <p>UUID: {{ $route.query.uuid }}</p>

        <label>Feeling</label>
        <textarea v-model="feeling"></textarea>

        <label>Prior Work</label>
        <textarea v-model="prior_work"></textarea>

        <label>Planned Work</label>
        <textarea v-model="planned_work"></textarea>

        <label>Blockers</label>
        <textarea v-model="blockers"></textarea>


        <button @click="sumbitForm">Submit</button>
        <p v-if="postCode == 200" class="success">Object Created</p>
        <p v-if="postCode == 400" class="error">Error.</p>
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
    input, textarea {
        display: block;
        padding: 10px 6px;
        width: 100%;
        box-sizing: border-box;
        border: none;
        border-bottom: 2px solid #ddd;
    }
    button {
        margin-top: 15px;
    }
    .success {
        color:green;
    }
    .error {
        color: red;
    }
</style>
