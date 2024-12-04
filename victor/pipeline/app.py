# app.py

import os
import time
import streamlit as st
from streamlit_timeline import st_timeline
import uuid

# Import other modules
from extract_file_to_txt import extract_text
from clean_txt import process_file
from text_chunking import TextChunker
from ner_processing import NerProcessor
from ner_postprocessing import postprocess_ner_results
from ollama_model_processor import OllamaModelProcessor
from date_classifier import retrieve_date_events
from date_converter import convert_dates
from extract_timeline_data import get_timeline_data
from utils import read_json_file

# Special effects
wait_time = 2
legal_document_types_path = "legal_document_types.json"
model_options_path = "model_options.json"

# Function to process the file step by step
def run_pipeline(file_name, upload_folder, process_folder, start_step=1, file_path = None, document_type="", related_events = None, ollama_key = None):
    if not file_path:
        # Initialize a dictionary to store intermediate results
        file_path = os.path.join(process_folder, upload_folder, file_name)

    # Step 1: Convert to text
    if start_step <= 1:
        st.write("### Step 1: Converting file to txt")
        with st.spinner(text="In progress..."):
            time.sleep(wait_time)
            try:
                text_files_folder = os.path.join(process_folder, 'text_files')
                os.makedirs(text_files_folder, exist_ok=True)
                step_1_file_path = extract_text(file_path, text_files_folder)
                st.write(f"Text file saved to `{step_1_file_path}`")

                st.success("Step 1 completed successfully.")

                file_path = step_1_file_path
            except Exception as e:
                st.error(f"Step 1 failed: {e}")
                if st.button("Re-run Step 1"):
                    run_pipeline(file_name, upload_folder, process_folder, start_step=1, file_path=file_path, document_type=document_type, related_events=related_events, ollama_key=ollama_key)
                return 

    # Step 2: Cleaning the Text Files
    if start_step <= 2:
        st.write("### Step 2: Cleaning Text File")
        with st.spinner(text="In progress..."):
            time.sleep(wait_time)
            try:
                cleaned_text_files_folder = os.path.join(process_folder, 'cleaned_text_files')
                os.makedirs(cleaned_text_files_folder, exist_ok=True)

                # Process the extracted text file
                step_2_file_path = process_file(file_path, cleaned_text_files_folder)
                st.write(f"Cleaned text saved to `{step_2_file_path}`")

                st.success("Step 2 completed successfully.")
                st.write("#### Cleaned Text Preview:")
                with open(step_2_file_path, 'r', encoding='utf-8') as f:
                    cleaned_file = f.read()
                st.write(cleaned_file[:500] + '...')  # Show a preview of the cleaned text

                file_path = step_2_file_path
            
            except Exception as e:
                st.error(f"Step 2 failed: {e}")
                if st.button("Re-run Step 2"):
                    run_pipeline(file_name, upload_folder, process_folder, start_step=2, file_path=file_path, document_type=document_type, related_events=related_events, ollama_key=ollama_key)
                return
        
    # Step 3: Chunking Text
    if start_step <= 3:
        st.write("### Step 3: Chunking Text")
        with st.spinner(text="In progress..."):
            time.sleep(wait_time)
            try:
                # Create a folder to save the chunked text
                chunked_text_folder = os.path.join(process_folder, 'chunked_text')
                os.makedirs(chunked_text_folder, exist_ok=True)

                # Initialize the TextChunker object
                text_chunker = TextChunker(output_folder=chunked_text_folder) # It uses the default tokenizer 'xlm-roberta-base' by default, but we can use the agomez302/nlp-dr-ner too:
                # text_chunker = TextChunker(tokenizer_name='agomez302/nlp-dr-ner', output_folder=chunked_text_folder)

                step_3_file_path, number_of_chunks, first_chunk = text_chunker.generate_chunks_file(file_path)
                st.write(f"Chunked text saved to `{step_3_file_path}`")
                st.success("Step 3 completed successfully.")
                st.write("#### Chunked Text:")
                st.write(f"Number of chunks created: {number_of_chunks}")
                st.write("Preview of first chunk:")
                st.write(first_chunk + '...')  # Show a preview of the first chunk
                
                file_path = step_3_file_path

            except Exception as e:
                st.error(f"Step 3 failed: {e}")
                if st.button("Re-run Step 3"):
                   run_pipeline(file_name, upload_folder, process_folder, start_step=3, file_path=file_path, document_type=document_type, related_events=related_events, ollama_key=ollama_key)
                return

    # Step 4: Run the NER model to extract dates from the chunks
    if start_step <= 4:
        st.write("### Step 4: Running NER Model")
        with st.spinner(text="In progress..."):
            try:
                # Create a folder to save the ner results
                ner_results_folder = os.path.join(process_folder, 'ner_results')
                os.makedirs(ner_results_folder, exist_ok=True)

                # Initialize the TextChunker object
                ner_processor = NerProcessor(output_folder=ner_results_folder) # It uses the trained model agomez302/nlp-dr-ner by default.

                step_4_file_path, first_result = ner_processor.generate_ner_predictions(file_path)
                st.write(f"NER results saved to `{step_4_file_path}`")
                st.success("Step 4 completed successfully.")
                st.write(f"Preview of the first result:") 
                st.write(first_result)
                
                file_path = step_4_file_path

            except Exception as e:
                st.error(f"Step 4 failed: {e}")
                if st.button("Re-run Step 4"):
                   run_pipeline(file_name, upload_folder, process_folder, start_step=4, file_path=file_path, document_type=document_type, related_events=related_events, ollama_key=ollama_key)
                return

    # Step 5: Post-processing the NER results
    if start_step <= 5:
        st.write("### Step 5: Post-processing NER Results")
        with st.spinner(text="In progress..."):
            time.sleep(wait_time)
            try:
                # Create a folder to save the post-processed ner results
                ner_postprocess_folder = os.path.join(process_folder, 'ner_postprocess_results')
                os.makedirs(ner_postprocess_folder, exist_ok=True)

                # Define path to cleaned text file
                cleaned_text_file_path = os.path.join(process_folder, 'cleaned_text_files', file_name) if not step_2_file_path else step_2_file_path
                
                step_5_file_path, first_result = postprocess_ner_results(file_path, cleaned_text_file_path, ner_postprocess_folder) # Context window is 400 by default
                st.write(f"NER postprocess results saved to `{step_5_file_path}`")
                st.success("Step 5 completed successfully.")
                st.write(f"Preview of the first result:") 
                st.write(first_result)
                
                file_path = step_5_file_path

            except Exception as e:
                st.error(f"Step 5 failed: {e}")
                if st.button("Re-run Step 5"):
                   run_pipeline(file_name, upload_folder, process_folder, start_step=5, file_path=file_path, document_type=document_type, related_events=related_events, ollama_key=ollama_key)
                return

    # Step 6: Classify Dates using LLM
    if start_step <= 6:
        st.write("### Step 6: Classifying Dates using LLM")        
        with st.spinner(text="Processing dates with the selected model..."):
            try:
                # Create a folder to save the model output
                model_output_folder = os.path.join(process_folder, f"classified_dates/{ollama_key}")
                os.makedirs(model_output_folder, exist_ok=True)

                model_hyperparameters = {
                    "temperature": 0.0000000000001
                    ,"top_k": 5
                    ,"top_p": 0.5
                    ,"seed": 42
                }

                execution_notes="Streamlit Test"
                model_download_path=None

                ollama_model = OllamaModelProcessor(model_name=ollama_key, model_storage_path=model_download_path, **model_hyperparameters)
                       

                step_6_file_path, first_result = retrieve_date_events(file_path, model_output_folder, document_type, related_events, ollama_model, model_hyperparameters, execution_notes=execution_notes)
                
                st.write(f"Date events saved to `{step_6_file_path}`")
                st.success("Step 6 completed successfully.")
                st.write(f"Preview of the first result:") 
                st.write(first_result)
                
                file_path = step_6_file_path

            except Exception as e:
                st.error(f"Step 6 failed: {e}")
                if st.button("Re-run Step 6"):
                   run_pipeline(file_name, upload_folder, process_folder, start_step=6, file_path=file_path, document_type=document_type, related_events=related_events, ollama_key=ollama_key)
                return
            
    # Step 7: Normalize Dates using LLM
    if start_step <= 7:
        st.write("### Step 7: Normalizing Dates using LLM")
        with st.spinner(text="Processing dates with the selected model..."):
            try:
                # Create a folder to save the model output
                model_output_folder = os.path.join(process_folder, f"normalized_dates/{ollama_key}")
                os.makedirs(model_output_folder, exist_ok=True)

                model_hyperparameters = {
                    "temperature": 0.0000000000001
                    ,"top_k": 5
                    ,"top_p": 0.5
                    ,"seed": 42
                }

                execution_notes="Streamlit Test normalizer"
                model_download_path=None

                ollama_model = OllamaModelProcessor(model_name=ollama_key, model_storage_path=model_download_path, **model_hyperparameters)
                       

                step_7_file_path, first_result = convert_dates(file_path, model_output_folder, ollama_model, execution_notes=execution_notes)
                
                st.write(f"Date events saved to `{step_7_file_path}`")
                st.success("Step 7 completed successfully.")
                st.write(f"Preview of the first result:") 
                st.write(first_result)
                
                file_path = step_7_file_path

            except Exception as e:
                st.error(f"Step 7 failed: {e}")
                if st.button("Re-run Step 7"):
                   run_pipeline(file_name, upload_folder, process_folder, start_step=7, file_path=file_path, document_type=document_type, related_events=related_events, ollama_key=ollama_key)
                return
            
    # Step 8: Normalize Dates using LLM
    if start_step <= 8:
        # Finally, we will be displaying the results in a timeline
        st.write("### Step 8: Displaying Results")
        try:
            # Create a folder to save the model output
            output_folder = os.path.join(process_folder, 'timeline_data')
            os.makedirs(output_folder, exist_ok=True)

            step_8_file_path, timeline_items = get_timeline_data(file_path, output_folder)
            
            st.write(f"Timeline data points saved to `{step_8_file_path}`")
            st.success("Step 8 completed successfully.")
            
            st.write(f"Timeline view")
            timeline = st_timeline(timeline_items, groups=[], options={}, height="500px", width="100%")
            st.subheader("Selected item")
            st.write(timeline) 
            
            file_path = step_8_file_path

        except Exception as e:
            st.error(f"Step 8 failed: {e}")
            if st.button("Re-run Step 8"):
                run_pipeline(file_name, upload_folder, process_folder, start_step=7, file_path=file_path, document_type=document_type, related_events=related_events, ollama_key=ollama_key)
            return

        
def main():
    st.title(":judge: Legal Document Date Extraction")
    st.subheader("An NLP-based tool to extract dates from legal documents in Spanish.")
    st.write("Please upload a legal document in Spanish to extract and classify dates.")

    uploaded_file = st.file_uploader("**Choose a file**", type=['pdf','doc', 'docx', 'txt'])

    # ------------------------------ 
    # Now we request the user to select the legal document type:
    # Load legal document types from JSON file
    legal_document_types = read_json_file(legal_document_types_path)
    
    # Extract list of types
    document_types = [item['type'] for item in legal_document_types]
    selected_document_type = st.selectbox("**Select the type of legal document**", document_types)
    
    # Find the selected document type in the list to get the related events
    selected_document_info = next((item for item in legal_document_types if item['type'] == selected_document_type), None)
    if selected_document_info:
        events = selected_document_info.get('events', [])
        st.write("**Related events**")
        events_str = ""
        for event in events:
            if not events_str:
                events_str += f"{event}"
            else:
                events_str += f"\t- {event}" 
        st.write(events_str)
    else:
        st.error("Selected document type not found in legal document types.")
        return
    
    # ------------------------------
    # Load model options from JSON file
    model_options = read_json_file(model_options_path)

    # Extract list of model names
    model_names = [item['model_name'] for item in model_options]
    
    selected_model_name = st.selectbox("Select model for classification:", model_names)
    
    # Find the selected model in the list to get the ollama_key
    selected_model_info = next((item for item in model_options if item['model_name'] == selected_model_name), None)
    if selected_model_info:
        ollama_key = selected_model_info['ollama_key']
    else:
        st.error("Selected model not found in model options.")
        return
    
    # Start processing
    if uploaded_file is not None:
        if st.button("Start"):
        
            # Naming for the folder containing the uploaded file
            upload_folder = 'docs'
            
            # Create a unique folder for this process run
            process_id = str(uuid.uuid4())
            process_folder = os.path.join('process_runs', process_id)
            # Create process folder
            os.makedirs(process_folder, exist_ok=True)
            # Create upload folder in process folder
            os.makedirs(os.path.join(process_folder, upload_folder), exist_ok=True)

            # Save the uploaded file
            file_path = os.path.join(process_folder, upload_folder, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File uploaded successfully and saved to `{process_folder}`.")

            run_pipeline(
                file_name=uploaded_file.name, 
                upload_folder=upload_folder, 
                process_folder=process_folder,
                document_type=selected_document_type,
                related_events=events,
                ollama_key=ollama_key
                )

if __name__ == "__main__":
    main()
