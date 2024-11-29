import os
import time
import streamlit as st
import uuid

# Import other modules
from extract_file_to_txt import extract_text
from clean_txt import process_file
from text_chunking import TextChunker
from ner_processing import NerProcessor
from ner_postprocessing import postprocess_ner_results

# Special effects
wait_time = 2

# Function to process the file step by step
def run_pipeline(file_name, upload_folder, process_folder, start_step=1, file_path = None):
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
                    run_pipeline(file_name, upload_folder, process_folder, start_step=1, file_path=file_path)
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
                    run_pipeline(file_name, upload_folder, process_folder, start_step=2, file_path=file_path)
                return
        
    # Step 3: Chunking Text
    if start_step <= 3:
        st.write("### Step 3: Chunking Text")
        with st.spinner(text="In progress..."):
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
                   run_pipeline(file_name, upload_folder, process_folder, start_step=3, file_path=file_path)
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
                   run_pipeline(file_name, upload_folder, process_folder, start_step=4, file_path=file_path)
                return

    # Step 5: Post-processing the NER results
    if start_step <= 5:
        st.write("### Step 5: Post-processing NER Results")
        with st.spinner(text="In progress..."):
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
                   run_pipeline(file_name, upload_folder, process_folder, start_step=5, file_path=file_path)
                return

    # # Step 6: With the edited chunks, run the LLM model to classify the date according to a given set of options.
    # st.write("### Step 3: Post-processing")
    # try:
    #     # Placeholder for Step 3 code
    #     # e.g., results['step3'] = postprocess(results['step2'])
    #     st.write("Post-processing data...")
    #     results['step3'] = "Post-processed data"

    #     # Save final result
    #     final_output_path = os.path.join(process_folder, 'final_output.txt')
    #     with open(final_output_path, 'w') as f:
    #         f.write(results['step3'])

    #     st.success("Step 3 completed successfully.")
    #     st.write("#### Final Output:")
    #     st.write(results['step3'])  # Display final output to the user
    # except Exception as e:
    #     st.error(f"Step 3 failed: {e}")
    #     if st.button("Re-run Step 3"):
    #         pipeline(file_path, process_folder)
    #     return

def main():
    st.title(":judge: Legal Document Date Extraction")
    st.subheader("An NLP-based tool to extract dates from legal documents in Spanish.")
    st.write("Please upload a legal document in Spanish to extract dates.")

    uploaded_file = st.file_uploader("Choose a file", type=['pdf','doc', 'docx', 'txt'])

    if uploaded_file is not None:
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

        # Start processing
        run_pipeline(file_name=uploaded_file.name, upload_folder=upload_folder, process_folder=process_folder)

if __name__ == "__main__":
    main()
