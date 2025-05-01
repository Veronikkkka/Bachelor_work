\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{caption}

\geometry{margin=1in}
\titleformat{\section}{\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\large\bfseries}{\thesubsection}{1em}{}

\title{\textbf{Bachelor Work Report}}
\author{}
\date{}

\definecolor{codegray}{gray}{0.95}
\lstset{
  backgroundcolor=\color{codegray},
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single
}

\begin{document}

\maketitle

\section*{Overview}

This work is based on \href{https://github.com/facebookresearch/dinov2}{DINOv2}, with the main implementation inside its submodule. Inspired by the RAW Adapter paper, the following concepts are adapted and modified:

\begin{itemize}
    \item Input-level adapter
    \item Model-level adapter
    \item Merge blocks
\end{itemize}

\section*{Added Files}

\subsection*{Configs}
\begin{itemize}
    \item \texttt{configs/train/custom.yaml}
\end{itemize}

\subsection*{Data}
\begin{itemize}
    \item \texttt{data/datasets/augmentation\_rggb.py}
    \item \texttt{data/datasets/knn\_for\_main.py}
    \item \texttt{data/datasets/main\_dataset.py}
    \item \texttt{data/datasets/my\_dataset.py}
    \item \texttt{data/datasets/npz\_raw.py}
    \item \texttt{data/datasets/pre\_process\_in\_advance.py}
    \item \texttt{data/datasets/pre\_processor.py}
    \item \texttt{data/datasets/raise\_dataset.py}
    \item \texttt{data/datasets/raw\_nod.py}
\end{itemize}

\subsection*{Evaluation}
\begin{itemize}
    \item \texttt{eval/segmentation1.py}
    \item \texttt{eval/segmentation2.py}
\end{itemize}

\subsection*{Models}
\begin{itemize}
    \item \texttt{models/help.py}
    \item \texttt{models/input\_level\_adapter.py}
\end{itemize}

\subsection*{Training}
\begin{itemize}
    \item \texttt{train/rgb\_to\_raw.py}
    \item \texttt{train/knn.py}
    \item \texttt{train/segmentation\_head.py}
\end{itemize}

\section*{Modified Files}

\begin{itemize}
    \item \texttt{configs/eval/vitb14\_pretrain.yaml}
    \item \texttt{data/transforms.py}
    \item \texttt{data/augmentations.py}
    \item \texttt{data/loaders.py}
    \item \texttt{eval/linear.py}
    \item \texttt{eval/utils.py}
    \item \texttt{models/vision\_transformer.py}
    \item \texttt{train/ssl\_meta\_arch.py}
    \item \texttt{train/train.py}
\end{itemize}

\section*{Dataset Structure}

The program expects input images in \textbf{RGGB format} as \texttt{.npy} files in the following structure:

\begin{lstlisting}
dataset/
├── train/
│   └── dataset_name/
│       └── images/
│           └── *.npy
├── val/
│   └── dataset_name/
│       └── images/
│           └── *.npy
└── test/
    └── dataset_name/
        └── images/
            └── *.npy
\end{lstlisting}

\section*{Commands}

\subsection*{Train Encoder}
\begin{lstlisting}[language=bash]
python3 -m dinov2.train.train \
  --config-file dinov2/configs/train/custom.yaml \
  --output-dir lala3
\end{lstlisting}

\subsection*{Run Linear Classifier}
\begin{lstlisting}[language=bash]
python3 -m dinov2.eval.linear \
  --config-file dinov2/configs/eval/vitb14_pretrain.yaml \
  --pretrained-weights lala3/model_0010499.rank_0.pth \
  --output-dir lalaa3/
\end{lstlisting}

\subsection*{Run Segmentation}
\begin{lstlisting}[language=bash]
CUDA_LAUNCH_BLOCKING=1 python3 -m dinov2.eval.segmentation2 \
  --train-dataset "Seg:root=/path/to/ADE20K/ADEChallengeData2016:split=train" \
  --val-dataset "Seg:root=/path/to/ADE20K/ADEChallengeData2016:split=val" \
  --pretrained-weights basic/model_0008999.rank_0.pth \
  --config-file dinov2/configs/eval/vitb14_pretrain.yaml \
  --output-dir seg_on_basic
\end{lstlisting}

\section*{Segmentation Examples}

You can include example images of segmentation results here:

\begin{figure}[h]
    \centering
    \fbox{\includegraphics[width=0.6\textwidth]{example_segmentation_1.png}}
    \caption{Example Segmentation Result 1}
\end{figure}

\begin{figure}[h]
    \centering
    \fbox{\includegraphics[width=0.6\textwidth]{example_segmentation_2.png}}
    \caption{Example Segmentation Result 2}
\end{figure}

\bigskip

\noindent\textit{Note: Replace the image filenames with your actual segmentation output screenshots.}

\end{document}
