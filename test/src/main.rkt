#lang racket

(require request/check
         "config.rkt")

(define auth-requester
  (make-domain-requester auth-service-domain
                         http-requester/exn))


(module+ test
  (with-requester auth-requester
    (check-get "/" "Hello!")))
