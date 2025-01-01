# My ollama

- [ollama](https://github.com/ollama/ollama)
- Start ollama:
  - [Work with installer terminal](#run-ollama-with-os-installer)
  - [Work with docker compose](#run-ollama-with-docker-compose)

## Run ollama with OS installer

  1. Download & install ollama depend OS: <https://ollama.com/download>

  2. Checking ollama: `ollama --help`

  3. Pull model: `ollama pull llama3.2`

  4. Check model list: open `ollama list`

  5. Run model: open `ollama run llama3.2`

  6. Try working:

     ```sh
     >>> ประเทศไทยมีกี่จังหวัด
     ```

     It should return something.

  7. Exit from model: type `/bye`

     ```sh
     >>> /bye
     ```

  8. You can also work with API: <https://github.com/ollama/ollama/blob/main/docs/api.md>

     For example:

     ```sh
     curl http://localhost:11434/api/generate -d '{
       "model": "llama3.2",
       "prompt": "ประเทศไทยมีกี่จังหวัด",
       "stream": false
     }'
     ```

## Run ollama with docker compose

  1. Build and run ollama with docker-compose by running:

     ```sh
     docker-compose up -d
     ```

  2. Check ollama status: open `http://localhost:11434`

     You can find all api in <https://github.com/ollama/ollama/blob/main/docs/api.md>
  3. Pull model:

     ```sh
     curl http://localhost:11434/api/pull -d '{
       "model": "llama3.2",
       "stream": false
     }'
     ```

  4. Check model list: open `http://localhost:11434/v1/models`
  5. Try working:

     ```sh
     curl http://localhost:11434/api/generate -d '{
       "model": "llama3.2",
       "prompt": "ประเทศไทยมีกี่จังหวัด",
       "stream": false
     }'
     ```

     It should return something like this:

     ```json
     {
       "model":"llama3.2",
       "created_at":"2025-01-01T06:09:43.436155154Z",
       "response":"ประเทศไทยมี 77 จังหวัด",
       "done":true,
       "done_reason":"stop",
       "context":[
         128006,
         9125,
         128007,
         271,
         38766,
         1303,
         33025,
         2696,
         25,
         6790,
         220,
         2366,
         18,
         271,
         128009,
         128006,
         882,
         128007,
         271,
         119556,
         27379,
         102737,
         48271,
         61516,
         107250,
         100736,
         128009,
         128006,
         78191,
         128007,
         271,
         119556,
         27379,
         29419,
         220,
         2813,
         100922,
         107250,
         100736
       ],
       "total_duration":752997624,
       "load_duration":23102347,
       "prompt_eval_count":32,
       "prompt_eval_duration":96000000,
       "eval_count":9,
       "eval_duration":632000000
     }
     ```
