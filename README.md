# SePR

[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
![](https://img.shields.io/badge/todo-2-blue)

*SePR* is a tool to Recognize Security Patches among open-source repository's patches.

## Journal

- [x]  script to extract CVE related patches.
- [x]  extract 32-dims features from vulnerability related patches.
- [x]  extract features from samples that *SPI: Automated Identification of Security Patches via Commits* offered .
- [x]  try to use One-Class SVM to learn patch mode.
- [x]  try to use full-connected neural network to recognize patches.
- [ ]  try to use static taint analysis on source code.
    - [x] control flow dependency analysis
    - [ ] variable‘s static taint analysis 
    - [ ] security constrains match analysis
- [ ]  try to use word2vec to classify git commit messages.


## So far Usage

1. **Generate *SeP* samples from a git repository**
```
$ python scripts/extract_cve_path.py -r ~/Documents/linux -t ./data/linux
```

See output examples in the following block

```
data
└── linux
    └── SeP
        └── ea81e2722e55ba0269c92f266763e445dcffb973
            ├── before
            │   ├── arch_s390_kernel_compat_ptrace.h
            │   ├── arch_s390_kernel_ptrace.c
            │   ├── drivers_s390_cio_chp.c
            │   ├── drivers_s390_cio_cio.c
            │   ├── drivers_s390_cio_css.c
            │   └── drivers_s390_cio_device_fsm.c
            ├── commit
            ├── patch
            └── patched
                ├── arch_s390_kernel_compat_ptrace.h
                ├── arch_s390_kernel_ptrace.c
                ├── drivers_s390_cio_chp.c
                ├── drivers_s390_cio_cio.c
                ├── drivers_s390_cio_css.c
                └── drivers_s390_cio_device_fsm.c
```
The script `excrat_cve_path.py` will automatically extract commits whose commit message contains strings like "CVE". 

Each commit will be placed in a directory, which mainly contains four items:
- before : files before patch
- patched: patched files
- commit : fuller text of commit message
- patch  : diff file between two commits


2. **Extract ASTs from codes** 

We use [astminer](https://github.com/JetBrains-Research/astminer) to extract Abstract Syntax Tree(AST) from the patch codes.

The `jar` package version of astminer is in the directory `static`.

```bash
$ java -jar astminer parse --lang c --project 
```



## TroubleShooting

### Errors when using astminer

Some jdk versions may occur errors when extracting ASTs in the step 2. 

An ideal way is using `java-8-openjdk`, the version that astminer's docker used.

```
$ archlinux-java status

Available Java environments:
  java-15-openjdk
  java-16-jdk
  java-8-openjdk (default)

```
