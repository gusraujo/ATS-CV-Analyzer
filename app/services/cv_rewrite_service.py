def rewrite_cv(
    llm_client,
    cv: dict,
    job: dict,
    match_result: dict
) -> dict:
    response = llm_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": CV_REWRITE_SYSTEM_PROMPT},
            {"role": "user", "content": build_cv_rewrite_prompt(cv, job, match_result)}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    return json.loads(content)
