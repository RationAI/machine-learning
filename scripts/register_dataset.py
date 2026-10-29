from kube_jobs import storage, submit_job


submit_job(
    job_name="project_name-register-dataset",
    username=...,
    image="cerit.io/rationai/base:2.0.6",
    cpu=1,
    memory="4Gi",
    public=False,
    script=[
        "git clone https://github.com/RationAI/project_name.git workdir",
        "cd workdir",
        "uv sync",
        "uv run python -c \"from rationai.provenance import register_dataset; print(register_dataset(csv='/mnt/data/.../cohort.csv', path_column='path', dataset_name='TODO', experiment_name='project_name'))\"",
    ],
    storage=[storage.secure.DATA, storage.secure.PROJECTS],
)
