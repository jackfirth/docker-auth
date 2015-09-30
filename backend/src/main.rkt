#lang racket

(require spin)

(get "/"
  (lambda () "Hello!"))

(run)
