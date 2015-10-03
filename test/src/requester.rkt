#lang racket

(provide auth-proxy-requester/basic
         auth-proxy-requester/jwt
         auth-api-requester
         backend-requester
         json-headers-requester)

(require fancy-app
         json
         request
         "config.rkt")


(define (add-requester-header header value requester)
  (add-requester-headers (list (format "~a: ~a" header value))
                         requester))

(define content-type-requester (add-requester-header "Content-Type" _ _))
(define accept-requester (add-requester-header "Accept" _ _))

(define jsexpr->bytes/utf-8 (compose string->bytes/utf-8 jsexpr->string))

(define auth-base-requester
  (make-domain-requester auth-service-domain
                         http-requester/exn))

(define auth-proxy-requester/basic
  (add-requester-headers (list (string-append "Authorization: Basic foo@bar.com:" test-password))
                         auth-base-requester))

(define auth-proxy-requester/jwt
  (add-requester-headers (list (string-append "Authorization: Bearer " test-jwt))
                         auth-base-requester))

(define json-headers-requester
  (compose (content-type-requester "application/json" _)
           (accept-requester "application/json" _)))

(define json-requester
  (compose json-headers-requester
           (wrap-requester-body jsexpr->bytes/utf-8 _)
           (wrap-requester-response string->jsexpr _)))

(define auth-api-requester
  (wrap-requester-location (string-append "auth/" _)
                           (json-requester auth-base-requester)))


(define backend-requester
  (make-domain-requester backend-service-domain
                         http-requester/exn))
