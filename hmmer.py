from pathlib import Path
import subprocess

def main():
    base_dir = Path(__file__).resolve().parent

    alignments_dir = base_dir / "domain_seeds"
    profiles_dir = base_dir / "profiles"
    results_dir = base_dir / "results"
    proteins_file = base_dir / "Myxococcus_xanthus_DK_1622_protein.faa"

    profiles_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    alignments = sorted(
        file for file in alignments_dir.iterdir()
        if file.suffix.lower() in {".seed"}
    )

    for alignment in alignments:
        domain = alignment.stem

        hmm_file = profiles_dir / f"{domain}.hmm"
        result_file = results_dir / f"{domain}.txt"

        print(f"Обработка домена: {domain}")

        # Построение HMM-профиля
        subprocess.run(
            ["hmmbuild", str(hmm_file), str(alignment)],
            check=True
        )

        # Поиск домена в протеоме бактерии
        with result_file.open("w") as output:
            subprocess.run(
                ["hmmsearch", str(hmm_file), str(proteins_file)],
                stdout=output,
                check=True
            )

        print(f"Готово: {domain}\n")

    print(f"\nОбработано доменов: {len(alignments)}")


if __name__ == "__main__":
    main()
