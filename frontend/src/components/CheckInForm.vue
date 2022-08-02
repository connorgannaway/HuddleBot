<script setup>
    import {onMounted, ref} from 'vue'
    import axios from 'axios'
    import { useRoute } from 'vue-router';

    const props = defineProps({
        inProgress: Array,
        testing: Array,
        done: Array,
    })

    const feeling = ref()
    const prior_work = ref()
    const planned_work = ref()
    const blockers = ref()

    const route = useRoute()
    const postCode = ref()

    
    //format form data and submit to backend api
    function sumbitForm(e){
        e.preventDefault()

        let plannedIDs = JSON.stringify(
            filterCheckboxes(props.inProgress)
        )
        let priorIDs = JSON.stringify(
            filterCheckboxes(
                props.testing.concat(props.done)
            )
        )
        
        let prior_work_string = priorIDs.concat(' ', prior_work.value)
        let planned_work_string = plannedIDs.concat(' ', planned_work.value)
        

        let params = {
            feeling: feeling.value,
            prior_work: prior_work_string,
            planned_work: planned_work_string,
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

    //return array of selected issues
    function filterCheckboxes(issues){
        console.log(issues)
        let arr = []
        for(var issue of issues){
            if(issue.working == 1){
                arr.push(issue.issuekey)
            }
        }
        
        return arr
    }



</script>



<template>

    <form>
        
        <h1>Daily Check-In</h1>
        <p>UUID: {{ $route.query.uuid }}</p>

        <label>Feeling</label>
        <textarea v-model="feeling"></textarea>

        <label>Prior Work</label>
        <div v-for="issue of props.testing">
            <span class="issue-checkbox">
                <input type="checkbox" @click="issue.working ^= true" />
                <p >{{issue.issuekey}}</p>
            </span>
        </div>
        <div v-for="issue of props.done">
            <span class="issue-checkbox">
                <input type="checkbox" @click="issue.working ^= true" />
                <p >{{issue.issuekey}}</p>
            </span>
        </div>
        <textarea v-model="prior_work"></textarea>

        <label>Planned Work</label>
        <div v-for="issue of props.inProgress">
            <span class="issue-checkbox">
                <input type="checkbox" @click="issue.working ^= true" />
                <p >{{issue.issuekey}}</p>
            </span>
        </div>
        <textarea v-model="planned_work"></textarea>

        <label>Blockers</label>
        <textarea v-model="blockers"></textarea>


        <button @click="sumbitForm" @click.prevent="submit">Submit</button>
        <p v-if="postCode == 200" class="success">Submitted</p>
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
        display: block;
        margin: 10px 0 5px;
        font-size: 1.2em;
        text-transform: uppercase;
        font-weight: normal;

    }
    input, textarea {
        display: block;
        padding: 10px 6px;
        width: 100%;
        box-sizing: border-box;
        border: none;
        border-radius: 10px;
        border-bottom: 2px solid #ddd;
        background-color: #eee;
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
    .issue-checkbox{
        display: inline-flex;
        padding: 5px;
        
    }
    .issue-checkbox input[type=checkbox]{
        vertical-align: middle;
        margin-right: 1em;
        height: 13px;
        margin: auto 0.5em ;
    }
    .issue-checkbox p {
        text-align: left;
        white-space: nowrap;
    }

</style>
